function counter(n) {
    const textarea = document.querySelectorAll('.num'+n);
    
    if (textarea[0].value.length>500) {
        textarea[0].value = textarea[0].value.substring(0,500);
    }
    textarea[1].innerHTML = textarea[0].value.length + '/500)';
};

// drag & drop
const portfolio = document.querySelector("#portfolio");
const uploadBox = document.querySelector("#dragBox");

    /* 박스 안에 Drag 들어왔을 때 */
    uploadBox.addEventListener('dragenter', function(e) {
    });
    
    /* 박스 안에 Drag를 하고 있을 때 */
    uploadBox.addEventListener('dragover', function(e) {
        e.preventDefault();

    });
    
    /* 박스 밖으로 Drag가 나갈 때 */
    uploadBox.addEventListener('dragleave', function(e) {

    });
    
    /* 박스 안에서 Drag를 Drop했을 때 */
    uploadBox.addEventListener('drop', function(e) {
        console.log("dd");
        e.preventDefault();
        const files = e.dataTransfer && e.dataTransfer.files;
        //files[0], files[1]식으로 파일 여러개 받아올 수 있음
        portfolio.files = files;
        console.log(files);

        // 추가된 파일을 어떻게 보여줄 것인지 여기에 구현
        
    });
