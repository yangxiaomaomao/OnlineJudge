#include <stdio.h>
#include <sys/time.h>
#include <stdlib.h>
#include "util.h"
#include "tree.h"


const char* forwardingtable = "project/test/forwarding-table.txt";

const char* basic_lookup  = "project/test/lookup_file.txt";
const char* basic_compare = "project/test/compare_file.txt";

const char* advanced_compare = "project/test/compare_file.txt";
const char* advanced_lookup  = "project/test/lookup_file.txt";



bool check_result(uint32_t* port_vec);

int main(void){
    struct timeval tv_start, tv_end;
    uint32_t* res1, *res2;
    
    printf("========Constructing the basic tree========\n");
    create_tree(forwardingtable_filename);

    // read test data should not be executed before create_tree, students will proceed
    // searching tree in the create tree func
    printf("========Reading data from basic lookup table========\n");
    uint32_t* basic_ip_vec = read_test_data(basic_lookup);

    // lookup and compute the interval
    printf("==========Looking up the basic port============\n");
    gettimeofday(&tv_start,NULL);
    basic_res = lookup_tree(ip_vec);
    gettimeofday(&tv_end,NULL);

    int  basic_pass     = check_result(basic_res, basic_compare);
    long basic_interval = get_interval(tv_start,tv_end);


    printf("========Constructing the advanced tree========\n");
    create_tree_advance(forwardingtable_filename);

    // read test data should not be executed before create_tree, students will proceed
    // searching tree in the create tree func
    printf("========Reading data from advanced lookup table========\n");
    uint32_t* advanced_ip_vec = read_test_data(advanced_lookup);

    // lookup and compute the interval
    printf("============Looking up the advanced port============\n");
    gettimeofday(&tv_start,NULL);
    advanced_res = lookup_tree_advance(advanced_ip_vec);
    gettimeofday(&tv_end,NULL);

    int  advanced_pass     = check_result(advanced_res, advanced_compare);
    long advanced_interval = get_interval(tv_start,tv_end);
    
    printf("=============dump result============\n");
    printf("basic_pass:%d\nbasic_lookup_time:%ldus\nadvance_pass:%d\nadvance_lookup_time:%ldus\n", \
            basic_pass,basic_interval,advance_pass,advance_interval);
    
    return 0;
}

bool check_result(uint32_t* port_vec, FILE* compare_filename){
    int port;
    FILE* fp = fopen(compare_filename,"r");

    if(NULL == fp){
        perror("Open compare file fails");
        exit(1);
    }

    for(int i = 0;i < TEST_SIZE;i++){
        fscanf(fp,"%d",&port);
        if(port != port_vec[i]){
            fclose(fp);
            return false;
        }
    }
    fclose(fp);

    return true;
}
