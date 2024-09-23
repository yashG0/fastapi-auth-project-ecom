// console.log("Hello from profile page")

const logoutBtn = document.getElementById("logoutBtn");

logoutBtn.addEventListener("click", (e) => {
  e.preventDefault();
  localStorage.removeItem("access_token");
  window.location.href = "/";
});

const updatePasswordField = document.getElementById("updatePasswordField");

updatePasswordField.addEventListener("submit", (e) => {
  e.preventDefault();
  // console.log("password being updated!");

  const newFormData = new FormData(updatePasswordField);
  const payload = {};
  newFormData.forEach((val, key) => {
    payload[key] = val;
  });
  // console.log(payload);
  if (payload) {
    updatePassword(payload);
  } else {
    alert("Enter the password and new password field!");
  }
});

const updatePassword = async (payload) => {
  try {
    const token = localStorage.getItem("access_token");
    if (!token) {
      alert("You must be logged in to update your password.");
      return;
    }

    const response = await fetch(
      "http://localhost:8000/api/user/updatePassword",
      {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
        },
        body: JSON.stringify({
          password: payload["currentPassword"],
          newPassword: payload["newPassword"],
        }),
      },
    );
    
    // const data = await response.json();
    if (response.ok){
      alert("Password has been updated Successfully!");
      window.location.href = "/api/auth/login-page"
    }else{
      alert("406: Failed to update password.");
    }
    
  } catch (err) {
    alert("An Error Occured! ", err);
    console.error("An Error Occured! ", err);
  }
};


const usernameDisplay = document.getElementById("usernameDisplay");
const emailDisplay = document.getElementById("emailDisplay");

window.addEventListener("load", async (e)=>{
  const token = localStorage.getItem("access_token");
  if (!token) {
    alert("You must be logged in to update your password.");
    return;
  }
  
  try{
    const res = await fetch("http://localhost:8000/api/user/userInfo", {
      method: "GET",
      headers: {
        Accept: "application/json",
        Authorization: `Bearer ${token}`,
      },
    });

    
    if (res.ok){
      const data = await res.json();
      console.log(data)
      usernameDisplay.innerText = data["username"]
      emailDisplay.innerText = data["email"]
    }
    
  }catch(err){
    console.error(err);
  }
})
