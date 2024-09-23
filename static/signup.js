// console.log("hello from signup")

const signup = document.getElementById("signupSubmit");


signup.addEventListener("submit", (e) => {
  e.preventDefault();

  // const username = document.getElementById("username").value;
  // const email = document.getElementById("email").value;
  // const password = document.getElementById("password").value;
  // const confirmPassword = document.getElementById("confirm_password").value;

  // console.log("Username:", username);
  // console.log("Email:", email);
  // console.log("Password:", password);
  // console.log("Confirm Password:", confirmPassword);

  const newSignupData = new FormData(signup);
  
  const payload = {};
  
  newSignupData.forEach((val,key)=>{
    payload[key] = val;
  })
  // console.log(payload);
  
  if (payload["password"] === payload["confirm_password"]){
    createUser(payload)
  }else{
    alert("Password do not match! please try again")
  }
  
});

const createUser = async (payload) => {
  try {
    const response = await fetch("http://localhost:8000/api/auth/signup", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify({username:payload["username"], email:payload["email"], password:payload["password"]}),
    });

    const data = await response.json();

    if (data.success) {
      window.alert(data.message); // Show success message in alert

      // You can also redirect the user to the login page after signup
      window.location.href = "/api/auth/login-page";
    } else {
      window.alert(data.detail || "An error occurred.");
    }
  } catch (err) {
    console.error("Error:", err);
    window.alert("An error occurred! Please try again.");
  }
};
