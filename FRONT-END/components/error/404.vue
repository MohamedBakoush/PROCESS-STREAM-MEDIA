<template> 
    <div class="gallery-section">
        <div class="swiper-container">
            <div class="swiper-gallery">
                <div class="swiper-wrapper">
                    <div class="swiper-slide">
                        <div class="slide-wrapper"> 
                            <div class="title-link">
                                <h2 class="project-title">404</h2>
                            </div>
                            <a href="/" class="location-text">Page not found</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>   
</template>

<style scoped>

/* Global Styles */
.gallery-section {
    display: flex;
    overflow: visible;
}

.swiper-container {
    max-width: 100%;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    position: fixed;
    left: 0;
    top: 0;
    right: 0;
    bottom: 0;
    margin: auto;
}

.swiper-wrapper {
    position: relative;
    width: 100%;
    height: 100%;
    z-index: 1;
    display: flex;
    transition-property: transform;
    box-sizing: content-box;
}

.swiper-slide {
    flex-shrink: 0;
    width: 100%;
    height: 100%;
    position: relative;
    transition-property: transform;
}

.title-link {
    font-size: 1em;
    text-decoration: none;
    background-color: transparent;
}

.project-title{ 
    font-size: 3.375em;
    line-height: .796296; 
    font-weight: bold;
}

.project-title, .location-text {
    position: relative;
    color: #000000;
    text-align: center;
    margin-top: 0;
    margin-bottom: 0;
    font-family: editorialnew, sans-serif;
}


.location-text::after {
    content: '';
    position: absolute;
    left: 0;
    bottom: 0;
    width: 0;
    height: 2px;
    background-color: currentColor;
    transition: width 0.3s ease;
    opacity: 1;
}

.location-text:hover::after {
    width: 100%;
}

.location-text {
animation-delay: 0.1s;
}

/* Responsive Design */
@media (max-width: 482px) {
    .location-text {
        text-align: center;
    }
}  
 
/* Additional Styles */
a {
    color: #ffffff;
    text-decoration: none;
}

h1, h2, h3, h4, h5, h6 {
    margin-bottom: 10px;
    font-weight: 700;
}

h2 {
    margin-top: 20px;
    font-size: 32px;
    line-height: 36px;
}

/* Ensure consistent margins and font sizes */
h2 {
    text-align: center;
    margin-top: 0;
    margin-bottom: 0;
    font-family: editorialnew, sans-serif;
    font-size: 2.19em;
    font-weight: 200;
    line-height: 1.13;
}
</style>