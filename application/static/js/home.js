//동영상 스크롤

const frameNumber = 0; // start video at frame 0
// 스크롤 길이 조절 상수
const playbackConst = 1500;
// DOM
const videoScroll = document.getElementById("video-scroll");
const vid = document.getElementById("v0");
var lastHeight = Math.floor(vid.duration)*playbackConst;
// dynamically set the page height according to video length
//????여기서 MAth.floor(vid...)을 lastHeight변수로 대체하면 제대로 작동이 안되네. vid.duration을 받아오기 전에 변수를 할당해서 그런거 같은데 어떻게 해결하지
vid.addEventListener("loadedmetadata", function () {
  videoScroll.style.height = Math.floor(vid.duration) * playbackConst + "px";
});

// Use requestAnimationFrame for smooth playback
function scrollPlay() {
  var frameNumber = window.pageYOffset / playbackConst;
  vid.currentTime = frameNumber;
  window.requestAnimationFrame(scrollPlay);
}

window.requestAnimationFrame(scrollPlay);

//스크롤 애니메이션
const onScroll = () => {
  const page1Comp = document.querySelectorAll(".pagecomp1");
  const page2Comp = document.querySelectorAll(".pagecomp2");
  const page3Comp = document.querySelectorAll(".pagecomp3");
  const page4Comp = document.querySelectorAll(".pagecomp4");
  const page5Comp = document.querySelectorAll(".pagecomp5");
  const title = document.querySelector("#logo-title");
  const vid = document.getElementById("v0");
  var lastHeight = Math.floor(vid.duration) * playbackConst;
  var currentY = document.querySelector("html").scrollTop;

  //스크롤 액션
  if (currentY >= 0 && currentY <= lastHeight / 5) {
    console.log(1);
    title.style.transform = `translate(${
      40 - ((40 * currentY) / lastHeight) * 5
    }rem,${20 - ((20 * currentY) / lastHeight) * 5}rem) scale(${
      550 - 450 * ((currentY / lastHeight) * 5)
    }%) `;
    for (comp of page1Comp) {
      comp.classList.add("none");
    }
    for (comp of page2Comp) {
      comp.classList.remove("none");
    }
  } else if (currentY > lastHeight / 5 && currentY <= (lastHeight / 5) * 2) {
    console.log(2);
    for (comp of page1Comp) {
      comp.classList.remove("none");
    }
    for (comp of page2Comp) {
      comp.classList.add("none");
    }
    for (comp of page3Comp) {
      comp.classList.remove("none");
    }
  } else if (
    currentY > (lastHeight / 5) * 2 &&
    currentY <= (lastHeight / 5) * 3
  ) {
    console.log(3);

    for (comp of page2Comp) {
      comp.classList.remove("none");
    }
    for (comp of page3Comp) {
      comp.classList.add("none");
    }
    for (comp of page4Comp) {
      comp.classList.remove("none");
    }
  } else if (
    currentY > (lastHeight / 5) * 3 &&
    currentY <= (lastHeight / 5) * 4
  ) {
    console.log(4);

    for (comp of page3Comp) {
      comp.classList.remove("none");
    }
    for (comp of page4Comp) {
      comp.classList.add("none");
    }
    for (comp of page5Comp) {
      comp.classList.remove("none");
    }
  } else if (currentY > (lastHeight / 5) * 4 && currentY <= lastHeight ) {
    console.log(5);

    for (comp of page4Comp) {
      comp.classList.remove("none");
    }
    for (comp of page5Comp) {
      comp.classList.add("none");
    }
  } else {
    for (comp of page5Comp) {
      comp.classList.remove("none");
    }
  }
};
window.addEventListener("load", onScroll);
window.addEventListener("scroll", onScroll);

//로딩화면
const delLoad = () => {
  setTimeout(() => {
    document.querySelector(".loading").style.display = "none";
    document.querySelector("#all").style.opacity = "100%";
    window.scrollTo(0,0);

  }, 2000);
  console.log("loaded");


};

