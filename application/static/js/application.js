

window.onload=()=>{
    counter(1)
    counter(2)
    counter(3)
    counter(4)
    counter(5)
}
function counter(n) {
    const textarea = document.querySelectorAll('.num'+n);
    textarea[1].innerHTML = textarea[0].value.length + '/500';


    if (textarea[0].value.length>500) {
        textarea[0].value = textarea[0].value.substring(0,500);
    }
    textarea[1].innerHTML = textarea[0].value.length + '/500';
};

// drag & drop
const portfolio = document.querySelector("#portfolio");
const design = document.querySelector("#design_doc");
const uploadBoxD = document.querySelector("#dragBoxD")
const uploadBoxP = document.querySelector("#dragBoxP");
const cancelD = document.querySelector(".cancelD");
const cancelP = document.querySelector(".cancelP");

    //파일 업로드 저장하기
    const getfile = (target)=>{
        const uploadbox = target==='portfolio'?uploadBoxP:uploadBoxD;
        // uploadbox.innerHTML=`${files[0]["name"]}`;
        const cancel = target==="portfolio"?cancelP:cancelD;
        console.log("filechanged");

        uploadbox.style.backgroundColor = "#04080F"
        uploadbox.style.fontSize = "3rem"
        cancel.style.display = "inline"

        uploadbox.innerHTML=`${target==="portfolio"?portfolio.value:design.value}`;
    }
    //x눌러서 취소
    const cancel = (target)=>{
        const inputFile = target==='portfolio'?portfolio:design;
        const uploadbox = target==='portfolio'?uploadBoxP:uploadBoxD;
        const cancelspan = target==='portfolio'?cancelP:cancelD;
        console.log("canceled")
        
        inputFile.value = null;
        uploadbox.style.backgroundColor = "rgba(255, 255, 255, 0.8)"
        uploadbox.style.fontSize = "2rem"
        uploadbox.innerHTML="Drag and Drop File Here"
        cancelspan.style.display = "none"
        
    }
    /* 박스 안에 Drag 들어왔을 때 */
    uploadBoxP.addEventListener('dragenter', function(e) {
    });
    
    /* 박스 안에 Drag를 하고 있을 때 */
    uploadBoxP.addEventListener('dragover', function(e) {
        e.preventDefault();

    });
    
    /* 박스 밖으로 Drag가 나갈 때 */
    uploadBoxP.addEventListener('dragleave', function(e) {

    });

    uploadBoxD.addEventListener('dragenter', function(e) {
    });
    
    /* 박스 안에 Drag를 하고 있을 때 */
    uploadBoxD.addEventListener('dragover', function(e) {
        e.preventDefault();

    });
    
    /* 박스 밖으로 Drag가 나갈 때 */
    uploadBoxD.addEventListener('dragleave', function(e) {

    });
    
    /* 박스 안에서 Drag를 Drop했을 때 -portfolio*/
    uploadBoxP.addEventListener('drop', function(e) {
        e.preventDefault();
        const files = e.dataTransfer && e.dataTransfer.files;
        //files[0], files[1]식으로 파일 여러개 받아올 수 있음
        portfolio.files = files;
        console.log("filedrop");
        // uploadBoxP.innerHTML=`${files[0]["name"]}`;
        getfile("portfolio");

    });

    /* 박스 안에서 Drag를 Drop했을 때 -design */
    uploadBoxD.addEventListener('drop', function(e) {
        e.preventDefault();
        const files = e.dataTransfer && e.dataTransfer.files;
        //files[0], files[1]식으로 파일 여러개 받아올 수 있음
        design.files = files;
        console.log("filedrop");
        // uploadBoxD.innerHTML=`${files[0]["name"]}`;
        getfile("design");

    });

