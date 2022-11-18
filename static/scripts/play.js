// Load video Button
const videoLoadButton = document.getElementById("upload-video");
// Upload video button
const videoUploadButton = document.getElementById("btn-upload-video");
// Input tag
const videoUploadFile = document.getElementById("upload-video-file-input");
console.log(videoUploadFile)
// Video Source element
const source = document.getElementById("ins-up-video-source");
// Video element
const videoElement = document.getElementById("video-element");

// Image Listing Button 
const imageListingButton = document.getElementById("image-listing");
// Image Listing Wrap 
const imageListingWrap = document.getElementById("images-list-wrap");

imageListingButton.addEventListener("click", ()=> {
    const coordinates = imageListingButton.getBoundingClientRect();
    imageListingWrap.style.display = "flex";
    imageListingWrap.style.top = coordinates.top + "px";
    imageListingWrap.style.left = coordinates.left + "px";
})

videoLoadButton.addEventListener("click", ()=> {
    videoUploadFile.click();
});

videoUploadFile.addEventListener("change", (event)=> {
    // File
    const videoFile = event.target.files[0];

    // Blob file
    const videoSrc = URL.createObjectURL(videoFile);

    // Set path
    source.src = videoSrc;

    // Load video
    videoElement.load();

    URL.revokeObjectURL(videoFile);

    // Upload the video to server
    videoUploadButton.click();
})


const hideFrame = document.getElementsByClassName("fa-bars-staggered");
const Frame = document.getElementById("output-wrap");

hideFrame.addEventListener("click", ()=>{
    Frame.style.right = "-36vw";
})
 