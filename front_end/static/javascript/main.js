let app = new Vue({
    el: '#app',
    data: {
        userData: {},
        usersID: 0,
        name: "",
        email: "",
        password: "",
        max_length: 25,
        max_pass_length: 16,
        max_tweet: 200,
        error: "",
        registered: false,
        tweetMsg: "",
        tweets: ["Hi","me","Hello","bad","boy","worst","something","blah","blah"]
    },
    methods: {
        registerAccount(){
            // record user details
            // add registration to localStorage
            // clear the registration fields

        }
    }
});

// function logFormSubmit(event){
//     console.log('Form submitted! Timestamp: ${event.timestamp}');
//     event.preventDefault();
// }

// const submitform =() => {
//     const form = document.getElementById('myform');
//     var x = document.getElementById("loader-wrapper");
//     // form.addEventListener('submit', () => {
//         console.log('Form submitted! Timestamp: ${event.timestamp}');
//         console.log(x)
//         x.style.display = "flex";
//     // });
// }

// function initialize(){
//     // const form = document.getElementById('myform');
//     // event.preventDefault();

//     document.getElementById("myform").addEventListener("submit", function(event){
//         event.preventDefault()
//     });
// }

// initialize()
    