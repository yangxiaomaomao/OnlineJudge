#include "tree.h"
#include <stdio.h>
#include <stdlib.h>

node_t* root;

node_t* init_node(){
    node_t* node = (node_t*)malloc(sizeof(node_t));
    node->port = -1;
    node->lchild = NULL;
    node->rchild = NULL;
    node->type   = I_NODE;
    return node;
}
// return an array of ip represented by an unsigned integer, size is TEST_SIZE
uint32_t* read_test_data(const char* lookup_file){
    FILE* fp = fopen(lookup_file,"r");

    if(NULL == fp){
        perror("Open lookup file fails");
        exit(1);
    }
    
	uint32_t* ip_vec = (uint32_t*)malloc(sizeof(uint32_t) * TEST_SIZE);
    for(int i = 0;i < TEST_SIZE;i++){
        
        uint32_t IP1 = 0,IP2 = 0,IP3 = 0,IP4 = 0;
        fscanf(fp,"%u.%u.%u.%u",&IP1,&IP2,&IP3,&IP4);

        ip_vec[i] = MASK(IP1,24) | MASK(IP2,16) | MASK(IP3,8) | MASK(IP4,0);
    }
    return ip_vec;
}

void insert_node(node_t* root,uint32_t ip,uint32_t mask_len,uint32_t port){
    int loc = ip >> 31;
    node_t* new_node = NULL;

    if(loc == LEFT&&root->lchild == NULL){
        new_node = init_node();
        root->lchild = new_node;
    }else if(loc == RIGHT&&root->rchild == NULL){
        new_node = init_node();
        root->rchild = new_node;
    }

    node_t* next_node = (loc == LEFT) ? root->lchild : root->rchild;
    if(mask_len == 1){
        next_node->type = M_NODE;
        next_node->port = port;
    }else{
        insert_node(next_node,ip << 1,mask_len - 1,port);
    }
}

void get_ip_info(FILE* fp,uint32_t* ip,uint32_t* mask_len,uint32_t* port){
    uint32_t IP1 = 0,IP2 = 0,IP3 = 0,IP4 = 0;
    fscanf(fp,"%u.%u.%u.%u %d %d",&IP1,&IP2,&IP3,&IP4,mask_len,port);
    *ip = MASK(IP1,24) | MASK(IP2,16) | MASK(IP3,8) | MASK(IP4,0);
}

void create_tree(const char* forward_file){
    FILE* fp = fopen(forward_file,"r");
    uint32_t ip,mask_len,port;
    
    node_t* new_node = init_node();
    for(int i = 0;i < TRAIN_SIZE;i++){
        get_ip_info(fp,&ip,&mask_len,&port);
        insert_node(new_node,ip,mask_len,port);
    }
    fseek(fp,0,SEEK_SET);
    root = new_node;
}


// return the port to forward
static uint32_t find_port(uint32_t ip){
    uint32_t port = -1; // init value
    node_t* root_save = root;
    while(root_save){
        if(root_save->type == M_NODE){
            port = root_save->port;
        }
        if(ip >> 31){
            root_save = root_save->rchild;
        }else{
            root_save = root_save->lchild;
        }
        ip <<= 1;
    }
    return port;
}
// Look up the ports of ip in file `lookup_file` using the basic tree
uint32_t *lookup_tree(uint32_t* ip_vec){
    uint32_t* ret = (uint32_t*)malloc(sizeof(uint32_t) * TEST_SIZE);
    //sleep(1);
    for(int i = 0;i < TEST_SIZE;i++){
        ret[i] = find_port(ip_vec[i]);
    }
    return ret;
}

void create_tree_advance(const char* forward_file){
    FILE* fp = fopen(forward_file,"r");
    uint32_t ip,mask_len,port;
    
    node_t* new_node = init_node();
    for(int i = 0;i < TRAIN_SIZE;i++){
        get_ip_info(fp,&ip,&mask_len,&port);
        insert_node(new_node,ip,mask_len,port);
    }
    fseek(fp,0,SEEK_SET);
    root = new_node;
}

// Look up the ports of ip in file `lookup_file` using the basic tree
uint32_t *lookup_tree_advance(uint32_t* ip_vec){
    uint32_t* ret = (uint32_t*)malloc(sizeof(uint32_t) * TEST_SIZE);
    //sleep(1);
    for(int i = 0;i < TEST_SIZE;i++){
        ret[i] = find_port(ip_vec[i]);
        //printf("port = %d\n",ret[i]);
    }
    return ret;
}




