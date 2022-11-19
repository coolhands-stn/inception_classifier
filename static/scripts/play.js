console.log("[play js]")
// Load video Button
const videoLoadButton = document.getElementById("upload-video");
// Upload video button
const videoUploadButton = document.getElementById("btn-upload-video");
// Input tag
const videoUploadFile = document.getElementById("upload-video-file-input");
// Video Source element
const source = document.getElementById("ins-up-video-source");
// Video element
const videoElement = document.getElementById("video-element");

// Image Listing Button 
const imageListingButton = document.getElementById("image-listing");
// Image Listing Wrap 
const imageListingWrap = document.getElementById("images-list-wrap");
// Hide frames listing button
hideFramesButton = document.querySelector(".fa-xmark");
// Show frames listing button
showFramesListingButton = document.getElementById("image-listing");


const codeParagraph = document.getElementById("code-p");
if(codeParagraph.textContent === "True"){
    showFramesListingButton.style.display = "flex";
    imageListingWrap.style.display = "flex";
}
// Show frames listing 
imageListingButton.addEventListener("click", ()=> {
    imageListingWrap.style.display = "flex";
})

// Hide frames listing 
hideFramesButton.addEventListener("click", ()=> {
    imageListingWrap.style.display = "none";
});

videoLoadButton.addEventListener("click", ()=> {
    videoUploadFile.click();
});

// Upload video,
// Load video as background
// show frames listing
videoUploadFile.addEventListener("change", (event)=> {
    imageListingWrap.style.display = "flex";
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

    // Show reveal frames button
    showFramesListingButton.style.display = "flex";
})