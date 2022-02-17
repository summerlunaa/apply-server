//글자수 세기
	//초기화
window.onload = () => {
	counter(1);
	counter(2);
	counter(3);
	counter(4);
};
	//입력시 글자수 갱신
function counter(n) {
	const textarea = document.querySelectorAll('.num' + n);
	textarea[1].innerHTML = textarea[0].value.length + '/500';

	if (textarea[0].value.length > 500) {
		textarea[0].value = textarea[0].value.substring(0, 500);
	}
	textarea[1].innerHTML = textarea[0].value.length + '/500';
}

// drag & drop
const portfolio = document.querySelector('#portfolio');
const design = document.querySelector('#design_doc');
const uploadBoxP = document.querySelector('#dragBoxP');
const cancelP = document.querySelector('.cancelP');
const filenameP = document.querySelector('#filenameP');
const fileaddP = document.querySelector('.fileaddP');

const uploadBoxD = document.querySelector('#dragBoxD');
const cancelD = document.querySelector('.cancelD');
const filenameD = document.querySelector('#filenameD');
const fileaddD = document.querySelector('.fileaddD');

	//파일 저장 후 ui변경
if (filenameP.innerHTML){
	uploadBoxP.style.display = 'none';
	fileaddP.style.display = 'flex';
}
if (filenameD!==null){
	if (filenameD.innerHTML){
		uploadBoxD.style.display = 'none';
		fileaddD.style.display = 'flex';
	}
}


const getfile = (target) => {
	const uploadbox = target === 'portfolio' ? uploadBoxP : uploadBoxD;
	const filename = target === 'portfolio' ? filenameP : filenameD;
	const fileadd = target === 'portfolio' ? fileaddP : fileaddD;
	console.log('filechanged');

	uploadbox.style.display = 'none';
	fileadd.style.display = 'flex';
	filename.innerHTML = `${
		target === 'portfolio' ? portfolio.value : design.value
	}`;
};
	//x눌러서 취소
const cancel = (target) => {
	const inputFile = target === 'portfolio' ? portfolio : design;
	const uploadbox = target === 'portfolio' ? uploadBoxP : uploadBoxD;
	const fileadd = target === 'portfolio' ? fileaddP : fileaddD;

	console.log('canceled');
	//파일 삭제 가능한지 확인 필요
	inputFile.value = null;

	uploadbox.style.display = 'block';
	fileadd.style.display = 'none';
};

	//이벤트리스너 추가 - portfolio
uploadBoxP.addEventListener('dragenter', function (e) {});
uploadBoxP.addEventListener('dragover', function (e) {
	e.preventDefault();
});
uploadBoxP.addEventListener('dragleave', function (e) {});
uploadBoxP.addEventListener('drop', function (e) {
	e.preventDefault();
	const files = e.dataTransfer && e.dataTransfer.files;
	portfolio.files = files;
	console.log('filedrop');
	getfile('portfolio');
});
	//이벤트리스너 추가 - design질문
if (uploadBoxD!==null){
    /* 박스 안에서 Drag를 Drop했을 때 -portfolio*/
    uploadBoxD.addEventListener('dragenter', function(e) {
    });
    uploadBoxD.addEventListener('dragover', function(e) {
        e.preventDefault();

    });
	uploadBoxD.addEventListener('dragleave', function(e) {
    });
    uploadBoxD.addEventListener('drop', function(e) {
        e.preventDefault();
        const files = e.dataTransfer && e.dataTransfer.files;
        design.files = files;
        getfile("design");
    });
}
