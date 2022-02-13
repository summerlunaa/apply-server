//동영상 재생
  //동영상 스크롤
const frameNumber = 0; // start video at frame 0
  // 스크롤 길이 조절 상수
const playbackConst = 1500;
  // DOM
const videoScroll = document.getElementById('video-scroll');
const vid = document.getElementById('v0');
var lastHeight = Math.floor(vid.duration) * playbackConst;
  // dynamically set the page height according to video length
vid.addEventListener('loadedmetadata', function () {
	videoScroll.style.height = Math.floor(vid.duration) * playbackConst + 'px';
});

  // Use requestAnimationFrame for smooth playback
function scrollPlay() {
	var frameNumber = window.pageYOffset / playbackConst;
	vid.currentTime = frameNumber;
	window.requestAnimationFrame(scrollPlay);
}

window.requestAnimationFrame(scrollPlay);
var pageNum = 1;

//스크롤 애니메이션
const page1 = document.querySelector('.page1');
	const page2 = document.querySelector('.page2');
	const page3 = document.querySelector('.page3');
	const page4 = document.querySelector('.page4');
	const page5 = document.querySelector('.page5');
	const title = document.querySelector('#logo-title');
	// const vid = document.getElementById('v0');
	const down = document.querySelector('#down');

const onScroll = () => {
	var lastHeight = Math.floor(vid.duration) * playbackConst;
	var currentY = document.querySelector('html').scrollTop;
	if (pageNum >= 6) {
		down.style.transform = 'rotate(180deg)';
	} else {
		down.style.transform = 'rotate(0deg)';
	}
	//스크롤 액션
	if (currentY >= 0 && currentY <= lastHeight / 5) {
		title.style.transform = `translate(${
			40 - ((40 * currentY) / lastHeight) * 5
		}rem,${18 - ((18 * currentY) / lastHeight) * 5}rem) scale(${
			550 - 450 * ((currentY / lastHeight) * 5)
		}%) `;

		page2.classList.remove('none');
		pageNum = 1;
	} else if (currentY > lastHeight / 5 && currentY <= (lastHeight / 5) * 2) {
		page2.classList.add('none');
		page3.classList.remove('none');
		title.style.transform = 'translate(0,0)';
		pageNum = 2;
	} else if (
		currentY > (lastHeight / 5) * 2 &&
		currentY <= (lastHeight / 5) * 3
	) {
		page3.classList.add('none');
		page2.classList.remove('none');
		page4.classList.remove('none');
		pageNum = 3;
	} else if (
		currentY > (lastHeight / 5) * 3 &&
		currentY <= (lastHeight / 5) * 4
	) {
		page4.classList.add('none');
		page3.classList.remove('none');
		page5.classList.remove('none');
		pageNum = 4;
	} else if (currentY > (lastHeight / 5) * 4 && currentY <= lastHeight) {
		page5.classList.add('none');
		page4.classList.remove('none');
		pageNum = 5;
	} else {
		page5.classList.remove('none');
		pageNum = 6;
	}
};
window.addEventListener('load', onScroll);
window.addEventListener('scroll', onScroll);
  //클릭시 스크롤
const downfunc = () => {
	const down = document.querySelector('#down');
	window.scrollTo({
		top:
			pageNum === 5
				? ((Math.floor(vid.duration) * playbackConst) / 5) *
				  (1 + pageNum++)
				: pageNum === 6
				? 0
				: ((Math.floor(vid.duration) * playbackConst) / 5) * pageNum +
				  1,
		behavior: 'smooth',
	});
};


//로딩화면
const delLoad = () => {
	// setTimeout(() => {
	// 	document.querySelector('.loading').style.display = 'none';
	// 	document.querySelector('#all').style.opacity = '100%';
	// 	window.scrollTo(0, 0);
	// }, 2000);
};
