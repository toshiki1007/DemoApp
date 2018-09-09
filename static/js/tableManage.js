function PageJump(){
    location.href = "https://6aa3afff7ffd44d48960862cecf60a83.vfs.cloud9.ap-southeast-1.amazonaws.com/";
}


function Counter(count){
    document.getElementById('counter').innerHTML = count;
    count--;
    setInterval(Counter(count),1000);
}