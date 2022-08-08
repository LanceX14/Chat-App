window.addEventListener("load", setup);

let timeoutID;
let timeout = 1000
let myTimeout;

function setup() {
	document.getElementById("new_message").addEventListener("click", makePost);
	show_all()
	timeoutID = window.setTimeout(show_all, timeout);
}

function show_all(){
	fetch("/messages/") 
	.then((response) => { 
		return response.json(); 
	}) 
	.then((results) => { 
		let chat_window = document.getElementById("chat_window"); 
		let messages = ""; 
		for (let index in results) { 
			current_set = results[index]; 
			messages += `User: ${current_set[0]}:\n${current_set[1]}\n\n`; 
		} 
		chat_window.value = messages; 
	}) 
	.catch(() => { 
		chat_window.value = "error retrieving messages from server"; 
	}); 
	timeoutID = window.setTimeout(show_all, timeout);
}

function makePost() {
	author = document.getElementById("the_username").innerHTML
	message = document.getElementById("the_message").value
	console.log(author+" message is "+message)

	fetch("/new_message/", { 
		method: "post", 
		headers: { "Content-type": "application/x-www-form-urlencoded; charset=UTF-8" }, 
		body: `username=${author}&message=${message}` 
	})
	.then((response) => response.json())
	.then((data) => {
		console.log('Success:', data);
	})
	.catch((error) => {
		console.error('Error:', error);
	});
	myTimeout = setTimeout(show_all, timeout);
}