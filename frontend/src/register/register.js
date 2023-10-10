// import * as Api from "/api.js";
import { validateEmail } from "../public/validateEmail";

const emailInput = document.querySelector("#email");
const passwordInput = document.querySelector("#password");
const passwordConfirmInput = document.querySelector("#passwordConfirmInput");
const fullNameInput = document.querySelector("#username");
const phoneNumberInput = document.querySelector("#phone");
// const postalCodeInput = document.querySelector("#postalCodeInput");
// const addressCity = document.querySelector("#addressCity");
// const addressDetail = document.querySelector("#addressDetail");
// const findAddressBtn = document.querySelector("#findAddressBtn");
const submitButton = document.querySelector("#submitButton");

addAllElements();
addAllEvents();

// html에 요소를 추가하는 함수들을 묶어주어서 코드를 깔끔하게 하는 역할임.
async function addAllElements() {}

// 여러 개의 addEventListener들을 묶어주어서 코드를 깔끔하게 하는 역할임.
function addAllEvents() {
  submitButton.addEventListener("click", handleSubmit);
  // findAddressBtn.addEventListener("click", searchAddress);
}

//주소 찾기
// function searchAddress() {
//     new daum.Postcode({
//         oncomplete: function (data) {
//             let addr = '';
//             let extraAddr = '';

//             if (data.userSelectedType === 'R') {
//                 addr = data.roadAddress;
//             } else {
//                 addr = data.jibunAddress;
//             }

//             if (data.userSelectedType === 'R') {
//                 if (data.bname !== '' && /[동|로|가]$/g.test(data.bname)) {
//                     extraAddr += data.bname;
//                 }
//                 if (data.buildingName !== '' && data.apartment === 'Y') {
//                     extraAddr +=
//                         extraAddr !== '' ? ', ' + data.buildingName : data.buildingName;
//                 }
//                 if (extraAddr !== '') {
//                     extraAddr = ' (' + extraAddr + ')';
//                 }
//             } else {
//             }

//             postalCodeInput.value = data.zonecode;
//             addressCity.value = `${addr} ${extraAddr}`;
//             addressDetail.focus();
//         },
//     }).open();
// }

// 회원가입 진행
async function handleSubmit(e) {
  e.preventDefault();

  const email = emailInput.value;
  const password = passwordInput.value;
  const passwordConfirm = passwordConfirmInput.value;
  const name = fullNameInput.value;
  const phone = phoneNumberInput.value;
  // const postalCode = postalCodeInput.value;
  // const address1 = addressCity.value;
  // const address2 = addressDetail.value;
  // const address = `(${postalCode}) ${address1} ${address2}`;

  // 입력 확인
  const isEmailValid = validateEmail(email);
  const num = password.search(/[0-9]/g);
  const eng = password.search(/[a-z]/gi);
  const spe = password.search(/[`~!@@#$%^&*|₩₩₩'₩";:₩/?]/gi);
  const isPasswordSame = password === passwordConfirm;
  const isFullNameValid = name.length >= 1;
  const phoneNum = /^[0-9]{2,3}-[0-9]{3,4}-[0-9]{4}$/;
  const isphoneNumber = phoneNum.test(phone);

  if (!isEmailValid) {
    return alert("이메일을 입력해주세요.");
  }

  if (password.length < 4 || password.length > 20) {
    return alert("4자리 이상 20자리 이내로 입력해주세요.");
  } else if (password.search(/\s/) != -1) {
    return alert("비밀번호는 공백 없이 입력해주세요.");
  } else if (num < 0 || eng < 0 || spe < 0) {
    return alert("영문, 숫자, 특수문자를 혼합하여 입력해주세요.");
  }

  if (!isPasswordSame) {
    return alert("비밀번호가 일치하지 않습니다.");
  }

  if (!isFullNameValid) {
    return alert("성함을 입력해주세요.");
  }

  if (!isphoneNumber) {
    return alert("연락처를 입력해주세요.");
  }

  try {
    const data = { email, password, name, phone };

    const join = await Api.post("/", data);
    localStorage.setItem("token", join.token);
    localStorage.setItem("loggedIn", "true");

    alert(`회원가입이 완료되었습니다.`);

    // 로그인 페이지 이동
    window.location.href = "../login";
  } catch (err) {
    console.error(err.stack);
  }
}
