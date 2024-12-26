// Definición de colores principales utilizados en la interfaz
const primaryColor = '#4834d4'  // Color primario (por ejemplo, para texto o elementos destacados)
const warningColor = '#f0932b'  // Color de advertencia (para mensajes de precaución)
const successColor = '#6ab04c'  // Color de éxito (para resultados positivos)
const dangerColor = '#eb4d4b'   // Color de peligro (para errores o alertas críticas)

// Nombres y valores relacionados con el tema (tema oscuro o claro)
const themeCookieName = 'theme'  // Nombre de la cookie para almacenar el tema
const themeDark = 'dark'         // Valor del tema oscuro
const themeLight = 'light'       // Valor del tema claro

// Referencia al elemento <body> del documento HTML
const body = document.getElementsByTagName('body')[0]

// Función para establecer cookies
function setCookie(cname, cvalue, exdays) {
  var d = new Date()
  d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000))  // Establece la fecha de expiración en días
  var expires = "expires=" + d.toUTCString()  // Convierte la fecha a formato UTC
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/"  // Define la cookie
}

// Función para obtener el valor de una cookie por su nombre
function getCookie(cname) {
  var name = cname + "="  // Formato esperado de la cookie
  var ca = document.cookie.split(';')  // Divide todas las cookies en un array
  for (var i = 0; i < ca.length; i++) {
    var c = ca[i]
    while (c.charAt(0) == ' ') {  // Elimina espacios en blanco iniciales
      c = c.substring(1)
    }
    if (c.indexOf(name) == 0) {  // Encuentra la cookie deseada
      return c.substring(name.length, c.length)
    }
  }
  return ""  // Retorna vacío si la cookie no existe
}

// Carga el tema al inicializar la página
loadTheme()

function loadTheme() {
  var theme = getCookie(themeCookieName)  // Obtiene el tema almacenado en la cookie
  body.classList.add(theme === "" ? themeLight : theme)  // Aplica el tema (por defecto, claro)
}

// Cambia entre el tema oscuro y claro
function switchTheme() {
  if (body.classList.contains(themeLight)) {  // Si el tema actual es claro
    body.classList.remove(themeLight)
    body.classList.add(themeDark)
    setCookie(themeCookieName, themeDark)  // Guarda el tema oscuro en la cookie
  } else {
    body.classList.remove(themeDark)
    body.classList.add(themeLight)
    setCookie(themeCookieName, themeLight)  // Guarda el tema claro en la cookie
  }
}

// Alterna la expansión/colapso de la barra lateral
function collapseSidebar() {
  body.classList.toggle('sidebar-expand')
}

// Evento que escucha clics en cualquier lugar de la ventana
window.onclick = function(event) {
  openCloseDropdown(event)  // Llama a la función para manejar desplegables
}

// Cierra todos los menús desplegables
function closeAllDropdown() {
  var dropdowns = document.getElementsByClassName('dropdown-expand')  // Obtiene los desplegables abiertos
  for (var i = 0; i < dropdowns.length; i++) {
    dropdowns[i].classList.remove('dropdown-expand')  // Cierra cada desplegable
  }
}

// Abre o cierra un menú desplegable basado en el evento
function openCloseDropdown(event) {
  if (!event.target.matches('.dropdown-toggle')) {
    // Si se hace clic fuera del menú desplegable, cierra todos los desplegables
    closeAllDropdown()
  } else {
    var toggle = event.target.dataset.toggle  // Obtiene el ID del menú relacionado
    var content = document.getElementById(toggle)  // Encuentra el contenido del desplegable
    if (content.classList.contains('dropdown-expand')) {
      closeAllDropdown()  // Si ya está abierto, lo cierra
    } else {
      closeAllDropdown()  // Cierra otros desplegables
      content.classList.add('dropdown-expand')  // Abre el seleccionado
    }
  }
}

// Configuración del gráfico (usando un elemento canvas con ID 'myChart')
var ctx = document.getElementById('myChart')
ctx.height = 500  // Altura del gráfico
ctx.width = 500   // Ancho del gráfico

// Datos para el gráfico
var data = {
  labels: [
    'January', 'February', 'April', 'May', 'June', 
    'July', 'August', 'September', 'October', 'November', 'December'
  ],  // Etiquetas para el eje X
  datasets: [
    {
      fill: false,  // No rellenar debajo de la línea
      label: 'Completed',  // Etiqueta del conjunto de datos
      borderColor: successColor,  // Color de la línea
      data: [120, 115, 130, 100, 123, 88, 99, 66, 120, 52, 59],  // Datos para el gráfico
      borderWidth: 2,  // Grosor de la línea
      lineTension: 0,  // Sin curva en las líneas
    },
    {
      fill: false,
      label: 'Issues',
      borderColor: dangerColor,
      data: [66, 44, 12, 48, 99, 56, 78, 23, 100, 22, 47],
      borderWidth: 2,
      lineTension: 0,
    }
  ]
}

// Inicialización del gráfico utilizando Chart.js
var lineChart = new Chart(ctx, {
  type: 'line',  // Tipo de gráfico: línea
  data: data,    // Datos a visualizar
  options: {
    maintainAspectRatio: false,  // No mantener la relación de aspecto
    bezierCurve: false,  // Líneas rectas sin curvas de Bézier
  }
})
