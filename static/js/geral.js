function menu() {
    const menu = document.getElementById('menu');
    menu.classList.toggle('show');
}






$(document).on('click', '.btn-menu', function (e) {
      e.preventDefault();
      const url = $(this).attr('href')

      $.get(url, function (data) {
            $('#conteudo-dinamico').html(data)
            window.history.pushState(null, null, url)
       
      })
             
});







  


