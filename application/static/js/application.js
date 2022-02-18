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
const checkboxP = document.querySelector('#portfolio-clear_id');
const checkboxD = document.querySelector('#design_doc-clear_id');

//파일 저장 후 ui변경
if (filenameP.innerHTML) {
	uploadBoxP.style.display = 'none';
	fileaddP.style.display = 'flex';
}
if (filenameD) {
	if (filenameD.innerHTML) {
		uploadBoxD.style.display = 'none';
		fileaddD.style.display = 'flex';
	}
}

const getfile = (target) => {
	const uploadbox = target === 'portfolio' ? uploadBoxP : uploadBoxD;
	const filename = target === 'portfolio' ? filenameP : filenameD;
	const fileadd = target === 'portfolio' ? fileaddP : fileaddD;
	const checkbox = target === 'portfolio' ? checkboxP : checkboxD;
	
	//체크박스 체크 풀기 - 파일 삭제 관련
	checkbox.checked = false;
	//ui그리기
	uploadbox.style.display = 'none';
	fileadd.style.display = 'flex';
	//파일명 보내기 - slicing
	filename.innerHTML = `${
		target === 'portfolio'
			? portfolio.value.slice(portfolio.value.lastIndexOf('\\')+1)
			: design.value.slice(design.value.lastIndexOf('\\')+1)
	}`;
	
};
//x눌러서 취소
const cancel = (target) => {
	const inputFile = target === 'portfolio' ? portfolio : design;
	const uploadbox = target === 'portfolio' ? uploadBoxP : uploadBoxD;
	const fileadd = target === 'portfolio' ? fileaddP : fileaddD;
	const checkbox = target === 'portfolio' ? checkboxP : checkboxD;
	
	//체크박스 체크풀기
	checkbox.checked = true;
		//선택하다가 '취소' 선택 시 onchange방지
	inputFile.value="";
	//ui그리기
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
if (uploadBoxD !== null) {
	/* 박스 안에서 Drag를 Drop했을 때 -portfolio*/
	uploadBoxD.addEventListener('dragenter', function (e) {});
	uploadBoxD.addEventListener('dragover', function (e) {
		e.preventDefault();
	});
	uploadBoxD.addEventListener('dragleave', function (e) {});
	uploadBoxD.addEventListener('drop', function (e) {
		e.preventDefault();
		const files = e.dataTransfer && e.dataTransfer.files;
		design.files = files;
		getfile('design');
	});
}
