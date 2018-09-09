function PageJump(){
    location.href = "http://ec2-52-77-80-183.ap-southeast-1.compute.amazonaws.com/";
}


function Counter(count){
    document.getElementById('counter').innerHTML = count;
    count--;
    setInterval(Counter(count),1000);
}
