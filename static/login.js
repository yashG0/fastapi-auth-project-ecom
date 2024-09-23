// console.log("hello from login js");

const loginSubmit = document.getElementById("loginSubmit");

loginSubmit.addEventListener("submit", async (e) => {
  e.preventDefault();

  const newFormData = new FormData(loginSubmit);
  if (newFormData) {
    const payload = {}
    newFormData.forEach((val,key) => {
      payload[key] = val
    })
    // console.log(payload)
    loginUser(payload);
  }
});

const loginUser = async (payload) => {
  try {
    const response = await fetch("/api/auth/login", {
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
        // console.log("Redirecting to profile page"); // Add logging to check if this runs
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
