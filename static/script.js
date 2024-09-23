const signup = document.getElementById("signupSubmit");
const login = document.getElementById("loginSubmit");

if (signup) {
  signup.addEventListener("submit", (e) => {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirm_password").value;

    // console.log("Username:", username);
    // console.log("Email:", email);
    // console.log("Password:", password);
    // console.log("Confirm Password:", confirmPassword);

    if (password === confirmPassword) {
      createUser({ username, email, password });
    } else {
      alert("Password do not match!");
    }
  });
}

if (login) {
  login.addEventListener("submit", (e) => {
    e.preventDefault();

    const usernameInput = document.getElementById("username");
    const passwordInput = document.getElementById("password");

    const username = usernameInput.value;
    const password = passwordInput.value;

    if (usernameInput && passwordInput) {
      // console.log(username)
      // console.log(password)
      loginUser({ username, password });

      usernameInput.value = "";
      passwordInput.value = "";
    } else {
      alert("Username or password must be required!");
    }
  });
}

const createUser = async (payload) => {
  try {
    const response = await fetch("http://localhost:8000/api/auth/signup", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify(payload),
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

const loginUser = async (payload) => {
  try {
    const response = await fetch("http://localhost:8000/api/auth/login", {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({
        grant_type: "password",
        username: payload.username,
        password: payload.password,
        scope: "",
        client_id: "string",
        client_secret: "string",
      }),
    });

    if (response.ok) {
      const data = await response.json();
      console.log("Login successful:", data);

      if (data.access_token) {
        localStorage.setItem("access_token", data.access_token);
        console.log("Redirecting to profile page"); // Add logging to check if this runs
        window.location.href = "/api/user/profile-page"; // Redirect to profile page
      }
    } else {
      const errorData = await response.json();
      window.alert(errorData.detail || "Login failed. Please try again.");
    }
  } catch (err) {
    console.error(err);
    window.alert("An error occurred! Please try again.");
  }
};

// for update the password and get user info ->
const userInfoCard = document.getElementById("userInfoCard");

const getUserInfo = async () => {
  const token = localStorage.getItem("access_token");

  if (!token) {
    console.error("No token found");
    return;
  }

  try {
    const res = await fetch("http://localhost:8000/api/user/userInfo", {
      method: "GET",
      headers: {
        Accept: "application/json",
        Authorization: `Bearer ${token}`,
      },
    });

    if (!res.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await res.json();

    userInfoCard.innerHTML = `
      <div class="card-body text-center">
          <img src="https://picsum.photos/100" alt="Profile Picture" class="rounded-circle mb-3">
          <h5 class="card-title">Profile Information</h5>
          <p><strong>Username:</strong> ${data.username} </p>
          <p><strong>Email:</strong> ${data.email}</p>
      </div>
      `;
  } catch (err) {
    console.error(err.message);
  }
};

if (window.location.pathname === "/api/user/profile-page") {
  window.addEventListener("load", getUserInfo);
}


const updatePasswordField = document.getElementById("updatePasswordField");

if (updatePasswordField) {
  updatePasswordField.addEventListener("submit", async (e) => {
    e.preventDefault();

    const currentPassword = document.getElementById("currentPassword").value;
    const newPassword = document.getElementById("newPassword").value;

    try {
      const token = localStorage.getItem("access_token");
      if (!token) {
        alert("You must be logged in to update your password.");
        return;
      }

      const response = await fetch("http://localhost:8000/api/user/updatePassword", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
        },
        body: JSON.stringify({
          password: currentPassword,
          newPassword: newPassword,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        alert("Password updated successfully!");
        // Optionally clear the fields
        updatePasswordField.reset();
      } else {
        alert(data.detail || "Failed to update password.");
      }
    } catch (error) {
      console.error("Error updating password:", error);
      alert("An error occurred. Please try again.");
    }
  });
}

const logoutBtn = document.querySelector("#logoutBtn")
if (logoutBtn){
  logoutBtn.addEventListener("click",(e)=>{
    e.preventDefault();
    logout()
  })
}

const logout = () => {
  console.log("removing")
  localStorage.removeItem("access_token");
  window.location.href = "/"; 
}