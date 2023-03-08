import{p as e}from"./paginationlogic.22ec78bb.js";import"./index.4d66c970.js";import{_ as a}from"./notification.8e3fe923.js";import{d as l,r as t,b as o,q as n,c as d,i as u,k as s,A as i,F as r,g as m,p,e as c,h as f,l as g,n as h,a as w}from"./vendor.e45b1972.js";const V=g();p("data-v-014795a4");const v=h("密码"),b=h("权限"),_=h("删除"),C={class:"dialog-footer"},y=h("取 消"),k=h("确 定"),S=h("题目操作"),z=h("比赛操作"),I=h("用户管理"),U=h("其他"),x=h("设置为后台管理员"),P=u("span",null,"确定删除该用户吗？",-1),j={class:"dialog-footer"},q=h("取 消"),A=h("确 定");c();var D=l({expose:[],setup(l){let p=t([]),{currentPage:c,pageCount:g,pageSize:h,pageSizes:D,handlePage:E,handlePageSize:F}=e(p,{dataUrl:"/admin/user/list"}),L=-1;o((async()=>{E(c.value)}));let T=t(!1),B=t(!1),G=t(!1),H=t(""),J=n({form:null});t(!0),t(!0),t(!0),t(!0);let K=t([!1,!1,!1,!1,!1]),M=t(-1);async function N(){let e=(await w.get("admin/user/search",{params:{name:H.value.toString(),page:c.value.toString(),limit:h.value.toString()}})).data;g.value=parseInt(e.count),p.value=e.list}function O(e){Y(1==e?1:0,1)}function Q(e){Y(1==e?1:0,2)}function R(e){Y(1==e?1:0,3)}function W(e){Y(1==e?1:0,4)}function X(e){Y(1==e?1:0,5)}function Y(e,l){let t={data:{op:String(e),power:String(l),userId:String(M.value)}};w.post("/admin/user/power/change",t).then((e=>{200==e.code&&a({title:"成功",message:"修改成功",type:"success"})})).catch((function(e){K.value[l-1]=!K.value[l-1],alert(e)}))}return(e,l)=>{const t=m("el-table-column"),o=m("el-switch"),n=m("el-button"),Y=m("el-table"),Z=m("el-pagination"),$=m("el-input"),ee=m("el-form-item"),ae=m("el-form"),le=m("el-dialog"),te=m("el-checkbox");return f(),d(r,null,[u(Y,{data:s(p),style:{width:"100%",height:"calc(100vh - 135px)","margin-top":"0.6em","margin-bottom":"5px"},height:"style.height","cell-style":{padding:"4px 0px"},"header-cell-style":{padding:"8px 0px"},stripe:"",border:!0,fit:""},{default:V((()=>[u(t,{sortable:"",fixed:"",prop:"userId",label:"ID",width:"65"}),u(t,{sortable:"",fixed:"",prop:"name",label:"用户名",width:"150"}),u(t,{sortable:"",prop:"nick",label:"真实姓名",width:"150"}),u(t,{prop:"lastLoginTime",label:"最后登录时间",width:"200"}),u(t,{prop:"deleted",label:"禁止登录",width:"80"},{default:V((e=>[u(o,{"active-color":"#ff4949",onClick:l=>function(e){let l={data:{userId:String(e.userId),delete:String(0==e.deleted?1:0)}};w.post("/admin/user/prohibit",l).then((l=>{200==l.code&&(e.deleted=0==e.deleted?1:0,a({title:"成功",message:1==e.deleted?"已禁止用户 "+e.name+" 登录 ":"用户"+e.name+"已经可以正常登录",type:"success"}))})).catch((function(e){alert(e)}))}(e.row),value:1==e.row.deleted},null,8,["onClick","value"])])),_:1}),u(t,{label:"操作",width:"200"},{default:V((e=>[u(n,{type:"primary",size:"mini",onClick:a=>function(e){T.value=!0,J.form=e,J.form.newPassword="",J.form.newPassword2=""}(e.row)},{default:V((()=>[v])),_:2},1032,["onClick"]),u(n,{type:"success",size:"mini",onClick:a=>function(e){M.value=e.userId;let a={name:e.name};K.value=[!1,!1,!1,!1,!1],w.get("/admin/user/power/list",{params:a}).then((e=>{200==e.code&&(e.data.forEach((e=>{K.value[e-1]=!0})),G.value=!0)})).catch((function(e){alert(e)}))}(e.row)},{default:V((()=>[b])),_:2},1032,["onClick"]),u(n,{type:"danger",size:"mini",onClick:a=>function(e){B.value=!0,L=e.userId}(e.row)},{default:V((()=>[_])),_:2},1032,["onClick"])])),_:1})])),_:1},8,["data"]),u(Z,{background:"",onSizeChange:s(F),onCurrentChange:s(E),"current-page":s(c),"page-sizes":s(D),"page-size":s(h),layout:"total, sizes, prev, pager, next, jumper",total:s(g)},null,8,["onSizeChange","onCurrentChange","current-page","page-sizes","page-size","total"]),u($,{placeholder:"搜索",modelValue:s(H),"onUpdate:modelValue":l[1]||(l[1]=e=>i(H)?H.value=e:H=e),size:"small",style:{width:"20em",height:"1em","margin-top":"-2.3em",float:"right"}},{append:V((()=>[u(n,{icon:"el-icon-search",onClick:N})])),_:1},8,["modelValue"]),u(le,{title:"修改密码",modelValue:s(T),"onUpdate:modelValue":l[8]||(l[8]=e=>i(T)?T.value=e:T=e)},{footer:V((()=>[u("span",C,[u(n,{onClick:l[6]||(l[6]=e=>i(T)?T.value=!1:T=!1)},{default:V((()=>[y])),_:1}),u(n,{type:"primary",onClick:l[7]||(l[7]=e=>function(){let e=J.form.newPassword,l=J.form.newPassword2,t=J.form.userId;if(""==e||""==l)a({title:"警告",message:"输入不能为空",type:"warning"});else if(e!=l)a({title:"警告",message:"两次密码输入不同",type:"warning"});else{T.value=!1;let l={data:{userId:String(t),password:e}};w.post("/admin/user/password/change",l).then((e=>{200==e.code&&a({title:"成功",message:"密码修改成功",type:"success"})})).catch((function(e){alert(e)}))}}())},{default:V((()=>[k])),_:1})])])),default:V((()=>[u(ae,{model:s(J).form},{default:V((()=>[u(ee,{label:"用户名"},{default:V((()=>[u($,{modelValue:s(J).form.name,"onUpdate:modelValue":l[2]||(l[2]=e=>s(J).form.name=e),disabled:!0},null,8,["modelValue"])])),_:1}),u(ee,{label:"用户id"},{default:V((()=>[u($,{modelValue:s(J).form.userId,"onUpdate:modelValue":l[3]||(l[3]=e=>s(J).form.userId=e),disabled:!0},null,8,["modelValue"])])),_:1}),u(ee,{label:"新密码"},{default:V((()=>[u($,{modelValue:s(J).form.newPassword,"onUpdate:modelValue":l[4]||(l[4]=e=>s(J).form.newPassword=e),"show-password":""},null,8,["modelValue"])])),_:1}),u(ee,{label:"重复新密码"},{default:V((()=>[u($,{modelValue:s(J).form.newPassword2,"onUpdate:modelValue":l[5]||(l[5]=e=>s(J).form.newPassword2=e),"show-password":""},null,8,["modelValue"])])),_:1})])),_:1},8,["model"])])),_:1},8,["modelValue"]),u(le,{title:"修改权限",modelValue:s(G),"onUpdate:modelValue":l[14]||(l[14]=e=>i(G)?G.value=e:G=e)},{default:V((()=>[u(te,{modelValue:s(K)[0],"onUpdate:modelValue":l[9]||(l[9]=e=>s(K)[0]=e),onChange:O},{default:V((()=>[S])),_:1},8,["modelValue"]),u(te,{modelValue:s(K)[1],"onUpdate:modelValue":l[10]||(l[10]=e=>s(K)[1]=e),onChange:Q},{default:V((()=>[z])),_:1},8,["modelValue"]),u(te,{modelValue:s(K)[2],"onUpdate:modelValue":l[11]||(l[11]=e=>s(K)[2]=e),onChange:R},{default:V((()=>[I])),_:1},8,["modelValue"]),u(te,{modelValue:s(K)[3],"onUpdate:modelValue":l[12]||(l[12]=e=>s(K)[3]=e),onChange:W},{default:V((()=>[U])),_:1},8,["modelValue"]),u(te,{modelValue:s(K)[4],"onUpdate:modelValue":l[13]||(l[13]=e=>s(K)[4]=e),onChange:X},{default:V((()=>[x])),_:1},8,["modelValue"])])),_:1},8,["modelValue"]),u(le,{title:"删除用户",modelValue:s(B),"onUpdate:modelValue":l[17]||(l[17]=e=>i(B)?B.value=e:B=e)},{footer:V((()=>[u("span",j,[u(n,{onClick:l[15]||(l[15]=e=>i(B)?B.value=!1:B=!1)},{default:V((()=>[q])),_:1}),u(n,{type:"primary",onClick:l[16]||(l[16]=e=>function(){let e={data:{userId:String(L)}};w.post("/admin/user/delete",e).then((e=>{200==e.code&&(a({title:"成功",message:"用户删除成功",type:"success"}),window.location.reload())})).catch((function(e){alert(e)})),B.value=!1,L=-1}())},{default:V((()=>[A])),_:1})])])),default:V((()=>[P])),_:1},8,["modelValue"])],64)}}});D.__scopeId="data-v-014795a4";export default D;
