const host=import.meta.env.VITE_LOGINHOST;

async function load_googlebtn() {
  try{
    const response = await fetch(`${host}/api/login/google`);
      if (response.ok){
        return response.json();
      }else{
        alert('Ошибка при создании авторизации через Google.Попробуйте обновить страницу');
      }
    }catch{
      alert('Ошибка при создании авторизации через Google.Попробуйте обновить страницу');
    };  
}
window.onload = () => {
  load_googlebtn().then(data => {
    if (data.url) {
      let google_button = document.createElement('button');
      google_button.id = "google-login";
      google_button.textContent = "Войти через Google";
    
      let svg = document.createElementNS("http://www.w3.org/2000/svg", 'svg');
      svg.setAttribute('xmlns', "http://www.w3.org/2000/svg");
      svg.setAttribute('x', "0px");
      svg.setAttribute('y', "0px");
      svg.setAttribute('width', "100");
      svg.setAttribute('height', "100");
      svg.setAttribute('viewBox', "0 0 48 48");
      svg.classList.add("google-logo");
    
      let path1 = document.createElementNS("http://www.w3.org/2000/svg", 'path');
      path1.setAttribute('fill', "#FFC107");
      path1.setAttribute('d', "M43.611,20.083H42V20H24v8h11.303c-1.649,4.657-6.08,8-11.303,8c-6.627,0-12-5.373-12-12c0-6.627,5.373-12,12-12c3.059,0,5.842,1.154,7.961,3.039l5.657-5.657C34.046,6.053,29.268,4,24,4C12.955,4,4,12.955,4,24c0,11.045,8.955,20,20,20c11.045,0,20-8.955,20-20C44,22.659,43.862,21.35,43.611,20.083z");
      svg.appendChild(path1);
    
      let path2 = document.createElementNS("http://www.w3.org/2000/svg", 'path');
      path2.setAttribute('fill', "#FF3D00");
      path2.setAttribute('d', "M6.306,14.691l6.571,4.819C14.655,15.108,18.961,12,24,12c3.059,0,5.842,1.154,7.961,3.039l5.657-5.657C34.046,6.053,29.268,4,24,4C16.318,4,9.656,8.337,6.306,14.691z");
      svg.appendChild(path2);
    
      let path3 = document.createElementNS("http://www.w3.org/2000/svg", 'path');
      path3.setAttribute('fill', "#4CAF50");
      path3.setAttribute('d', "M24,44c5.166,0,9.86-1.977,13.409-5.192l-6.19-5.238C29.211,35.091,26.715,36,24,36c-5.202,0-9.619-3.317-11.283-7.946l-6.522,5.025C9.505,39.556,16.227,44,24,44z");
      svg.appendChild(path3);
    
      let path4 = document.createElementNS("http://www.w3.org/2000/svg", 'path');
      path4.setAttribute('fill', "#1976D2");
      path4.setAttribute('d', "M43.611,20.083H42V20H24v8h11.303c-0.792,2.237-2.231,4.166-4.087,5.571c0.001-0.001,0.002-0.001,0.003-0.002l6.19,5.238C36.971,39.205,44,34,44,24C44,22.659,43.862,21.35,43.611,20.083z");
      svg.appendChild(path4);
  
      google_button.insertBefore(svg, google_button.firstChild);
    
      let login_div = document.getElementById('login-div');
      login_div.appendChild(google_button);
      google_button.addEventListener('click', function() {
        window.location.href = data.url;
      }); 
    };
  });
};

