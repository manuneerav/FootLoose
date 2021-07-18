
const url = window.location.href
console.log(url)
const searchBox = document.getElementById('search-form')
const searchInput = document.getElementById('search-input')
const resultsBox = document.getElementById('results-box')
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value
// const urlp = "http://127.0.0.1:8000";

console.log(csrf)

const sendSearchData = (name) => {
  $.ajax({
      type: 'POST',
      url:'http://127.0.0.1:8000/s/',
      data:{
        'csrfmiddlewaretoken':csrf,
        'name': name,
      },
      success: (res)=>{
          console.log(res)
      },
      error: (err)=>{
          console.log(err)
      }
  })
  }

  searchInput.addEventListener('keyup',e =>{
    console.log(e.target.value)
    if(resultsBox.classList.contains('not-visible')){
        resultsBox.classList.remove('not-visible')
    }

    sendSearchData(e.target.value)

  })
