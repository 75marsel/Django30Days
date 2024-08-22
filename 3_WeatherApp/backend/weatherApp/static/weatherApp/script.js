console.log("ok")

const url = window.location.href
const searchForm = document.getElementById("search-form")
const searchInput = document.getElementById("search-input")
const resultBox = document.getElementById("cards-container")

const csrf = document.getElementsByName("csrfmiddlewaretoken")[0].value
// console.log(csrf)

const sendSearchData = (search_query) => {
    // use ajax to send a post to the search/ url
    // must include the csrf token and the search query fetched by add event listener
    $.ajax({
        type: "POST",
        url: "search/",
        data: {
            "csrfmiddlewaretoken": csrf,
            "search_query": search_query,
        },
        // if success, get the data from response and change the inner html of the resultbox
        success: (res) => {
            const data = res.data
            
            resultBox.innerHTML = ""
            // if (data.length > 0) {      
                data.forEach(city=>{    
                    resultBox.innerHTML += ` 
                            <div class="card bg-base-100 w-full max-w-md mx-auto shadow-xl  scale-0 opacity-0 animate-fade" style="animation-delay: 0.1s;  max-height: 180px;">
                                <div class="grid grid-cols-4">
                                    <img
                                        class="w-full max-w-[200px] max-h-[200px] object-cover"
                                        src="http://openweathermap.org/img/w/${city.icon}.png"
                                        srcset="
                                        http://openweathermap.org/img/w/${city.icon}.png 1x,
                                        http://openweathermap.org/img/w/${city.icon}.png 2x"
                                        alt="Image"
                                    />
                                    <div class="card-body col-span-3">
                                        <h2 class="card-title">${city.city}</h2>
                                        <span>${city.temperature}° C</span>
                                        <p>${city.description}</p>
                                    </div>
                                </div>
                            </div>
                    `
                })
        },
        error: (err) => {
            console.log(err)
        }
    })
}

/*
    This function is for detecting the characters being typed in the search box
    allowing search to happen without refreshing the page!
*/
searchInput.addEventListener("keyup", e=>{
    console.log(e.target.value)

    if (resultBox.classList.contains("hidden")){
        resultBox.classList.remove("hidden")
    }

    sendSearchData(e.target.value)
})