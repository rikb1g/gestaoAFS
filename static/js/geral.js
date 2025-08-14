function menu() {
    const menu = document.getElementById('menu');
    menu.classList.toggle('show');
}


document.addEventListener('DOMContentLoaded', function() {
    const tooggleBtn = document.getElementById("theme-toggle");
    const body = document.body;

    // verificar a preferencia guardada
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme === "dark") {
        body.classList.add("dark-mode");
        tooggleBtn.textContent = "☀️ Claro" 
    } else if (savedTheme === "light") {
        body.classList.remove("dark-mode");
        tooggleBtn.textContent = "🌙 Escuro"
    } else {
      if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
        body.classList.add("dark-mode");
        tooggleBtn.textContent = "☀️ Claro" 
      }
    }

    tooggleBtn.addEventListener("click", function() {
       
      if(body.classList.contains("dark-mode")){
            body.classList.remove("dark-mode");
            tooggleBtn.textContent = "🌙 Escuro"
            localStorage.setItem("theme", "light");
            
      } else {
            body.classList.add("dark-mode");
            tooggleBtn.textContent = "☀️ Claro"
            localStorage.setItem("theme", "dark");
      }
        
    });
});


window.addEventListener('popstate', function(event) {
    this.location.reload();
});


$(document).on('click', '.btn-menu', function (e) {
      e.preventDefault();
      const url = $(this).attr('href')

      $.get(url, function (data) {
            $('#conteudo-dinamico').html(data)
            window.history.pushState(null, null, url)
       
      })
             
});







  


