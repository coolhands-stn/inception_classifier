console.log("[main.js]")

const predictedImage = document.getElementById("output-image");
const imageIndex = document.getElementById("image-index");

const imageName = parseInt(imageIndex.textContent);

if((imageName !== '') || (imageName !== null) ){
    predictedImage.src = `../static/frames/${imageName}.jpeg` 
}