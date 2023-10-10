// import * as Api from "/api.js";

const emailInput = document.querySelector("#email");
const passwordInput = document.querySelector("#password");
const submitButton = document.querySelector("#submitButton");

addAllElements();
addAllEvents();

// html에 요소를 추가하는 함수들을 묶어주어서 코드를 깔끔하게 하는 역할임.
async function addAllElements() {}

// 여러 개의 addEventListener들을 묶어주어서 코드를 깔끔하게 하는 역할임.
function addAllEvents() {
  submitButton.addEventListener("click", handleSubmit);
}

// 로그인 진행
async function handleSubmit(e) {
  e.preventDefault();

  const email = emailInput.value;
  const password = passwordInput.value;

  // 비밀번호 입력 확인
  const isPasswordValid = password.length >= 4;

  if (!isPasswordValid) {
    return alert("비밀번호는 4글자 이상 입력해주세요.");
  }

  // api 요청
  try {
    const data = { email, password };

    const result = await Api.post("", data);
    const token = result.token;
    console.log(token);

    // 토큰이 localStorage에 저장됨
    localStorage.setItem("token", token);
    localStorage.setItem("loggedin", "true");

    // 로그인 성공
    // 기본 페이지로 이동
    window.location.href = "../home";
  } catch (err) {
    console.error(err.stack);
    alert(`${err.message}`);
  }
}
