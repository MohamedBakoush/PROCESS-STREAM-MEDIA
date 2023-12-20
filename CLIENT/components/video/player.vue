<script setup>
// Refs for DOM elements
const ref_video = ref(null);
const ref_video_controls = ref(null);
const ref_video_container = ref(null);
const ref_volume_slider = ref(null);
const ref_progress_slider = ref(null);
const ref_volume_tool_tip = ref(null);

// video player states
const state_video = reactive({
    duration: 0,
    progress: 0,
    volume: 1,
    volumeBeforeMuted: 1,
    isPlaying: false,
    isMuted: false,
    isLoading: false,
    isVideoPayable: false,
    isVolumeHovered: false,
  }
); 

// Handel Video Metadata
const handleVideoMetadata = (event) => {  
  if (!ref_video.value) return;
  state_video.duration = ref_video.value.duration ?? 0;
};

// Video Playable
const onVideoCanPlay = (event) => {
  state_video.isLoading = false;
  state_video.isVideoPayable = true;
  console.log(false);
};

// Video Loading
const onVideoWaiting = () => { 
  state_video.isVideoPlayable = false; 
  if (!state_video.isLoading) return;  
  setTimeout(() => {
    if (!state_video.isVideoPlayable) {  
      state_video.isLoading = true;
    }
  }, 100); // Delay  
};

// Video Play/Pause
const toggleMediaPlayPause = () => { 
  resetPlaybackRate(); // Reset playback rate
  if (ref_video.value.paused) { // Toggle play/pause
    ref_video.value.play();
    state_video.isPlaying = true;
  } else {
    ref_video.value.pause();
    state_video.isPlaying = false;
  }
};

// Video Progress Time Update
const handleVideoTimeUpdate = () => {
  if (ref_video.value && !state_drag_video_controls.isDragging) {
    state_video.progress = ref_video.value.currentTime;
    updateVideoSliderProgress();
  } 
}

const onVideoProgressSliderInput = (event) => {  
  const newTime = parseFloat(event.target.value);
  if (ref_video.value) {
    ref_video.value.currentTime = newTime;  
  }
  state_video.progress = newTime;
  updateVideoSliderProgress();
}

const updateVideoSliderProgress = () => {  
  if (ref_video.value && ref_progress_slider.value) {
    const progress = (ref_video.value.currentTime / ref_video.value.duration) * 100;
    ref_progress_slider.value.style.setProperty('--video-slider-progress', `${progress}%`);
    ref_progress_slider.value.value = ref_video.value.currentTime.toString();
  } 
}

const calculateProgressSliderLoadingWidth = () => {
  // Calculate the percentage of the video unwatched
  const unwatchedPercentage = 100 - (state_video.progress / state_video.duration) * 100;
  return unwatchedPercentage;
};

const formatTime = (timeInSeconds) => {
  const minutes = Math.floor(timeInSeconds / 60);
  const seconds = Math.floor(timeInSeconds % 60);
  return `${minutes}:${seconds.toString().padStart(2, '0')}`; 
};

// Video Voume  
let hideVolumeSliderTimeout;

const updateVolumeSlider = (event) => {
  let newVolume;

  if (event && !isNaN(event.target.value)) {
    newVolume = parseFloat(event.target.value);
  } else if (ref_volume_slider.value && !isNaN(ref_volume_slider.value.value)) {
    newVolume = parseFloat(ref_volume_slider.value.value);
  } else {
    // Log an error if both conditions fail
    console.error('Invalid input for volume:', event ? event.target.value : 'undefined');
    return; // Exit the function as we can't proceed without a valid volume value
  }

  // Validate newVolume
  if (!isFinite(newVolume) || newVolume < 0 || newVolume > 1) {
    return; // Exit the function as the new volume value is not within the valid range
  }
  
  if (ref_video.value && ref_volume_slider.value && ref_volume_tool_tip.value) {
    ref_video.value.volume = newVolume;
    state_video.volume = newVolume;

    // Unmute and update the icon if the volume is adjusted while muted
    if (ref_video.value.muted && newVolume > 0) {
      ref_video.value.muted = false;
      state_video.isMuted = false; // Make sure this state is used for controlling the icon display
      state_video.volumeBeforeMuted = newVolume;
    }

    // Calculate and update tooltip position
    const sliderRect = ref_volume_slider.value.getBoundingClientRect();
    const thumbPosition = (newVolume / ref_volume_slider.value.max) * sliderRect.width;
    const tooltipOffset = ref_volume_tool_tip.value.offsetWidth / 2;
    let leftPosition = thumbPosition - tooltipOffset;
    leftPosition = Math.max(leftPosition, 0);
    leftPosition = Math.min(leftPosition, sliderRect.width - ref_volume_tool_tip.value.offsetWidth);
    ref_volume_tool_tip.value.style.left = `${leftPosition}px`;

    // Update slider visual representation
    const progress = (newVolume / ref_volume_slider.value.max) * 100;
    ref_volume_slider.value.style.setProperty('--volume-slider-progress', `${progress}%`);
    ref_volume_slider.value.value = newVolume;
    ref_volume_slider.value.style.backgroundSize = `${progress}% 100%`;
  }
};

const toggleMute = () => {
  if (ref_video.value && ref_volume_slider.value) {
    ref_video.value.muted = !ref_video.value.muted;
    state_video.isMuted = ref_video.value.muted;

    if (state_video.isMuted) {  
      state_video.volumeBeforeMuted = state_video.volume;
      state_video.volume = 0;
      ref_video.value.volume = 0;

      ref_volume_slider.value.style.setProperty('--volume-slider-progress', '0%');
      ref_volume_slider.value.style.backgroundSize = '0% 100%';
      ref_volume_slider.value.value = 0;  
    } else { 
      state_video.volume = state_video.volumeBeforeMuted;
      ref_video.value.volume = state_video.volumeBeforeMuted; 

      const volumePercent = state_video.volumeBeforeMuted * 100;
      ref_volume_slider.value.style.setProperty('--volume-slider-progress', `${volumePercent}%`);
      ref_volume_slider.value.style.backgroundSize = `${volumePercent}% 100%`;
      ref_volume_slider.value.value = state_video.volumeBeforeMuted;  
    }
  }
}; 

const handleMouseEnterVolumeControls = () => {
  clearTimeout(hideVolumeSliderTimeout); 
  state_video.isVolumeHovered = true;
  if (ref_volume_slider.value) {
    ref_volume_slider.value.style.display = 'block'; 
  }
};

const handleMouseLeaveVolumeControls = () => {
  state_video.isVolumeHovered = false;
  delayedHideVolumeSlider();
};

const delayedHideVolumeSlider = () => {
  clearTimeout(hideVolumeSliderTimeout);
  hideVolumeSliderTimeout = setTimeout(() => {
    if (!state_video.isVolumeHovered) {
      if (ref_volume_slider.value) {
        ref_volume_slider.value.style.display = 'none'; 
      }
    }
  }, 300);  
};

const handleRangeSliderMouseDown = (event) => {   
  if (event.srcElement.classList.contains('volume-slider')) {
    ref_volume_tool_tip.value.style.display = 'block';
    ref_volume_slider.value.classList.add('slider-active');
  } else if (event.srcElement.classList.contains('video-progress-slider')) {
    ref_progress_slider.value.classList.add('slider-active');
  }
};

const handleRangeSliderMouseUp = () => {   
  ref_volume_tool_tip.value.style.display = 'none';
  ref_volume_slider.value.classList.remove('slider-active');
  ref_progress_slider.value.classList.remove('slider-active');
};
 
// video player controls states
const state_video_controls = reactive({ 
  isFullscreen: false,
  isShowControls: false,
  isMouseOverControls: false,
  currentForwardSpeed: 1,
  currentBackwardSpeed: 1,
  avaiableBackwardSpeeds: [2, 3, 4],
  avaiableForwardSpeeds: [2, 3, 4],
  fastBackwardInterval: null,
  fastForwardInterval: null,
  mouseMoveTimeout: null,
});

// full screen
const toggleFullScreen = () => {
  if (!document.fullscreenElement) {
    ref_video_container.value.requestFullscreen().catch(err => {
      alert(`Error attempting to enable full-screen mode: ${err.message} (${err.name})`);
    });
    state_video_controls.isFullscreen = true;
  } else {
    if (document.exitFullscreen) {
      document.exitFullscreen();
    }
    state_video_controls.isFullscreen = false;
  }
};

//
const showVideoControls = () => {
  state_video_controls.isShowControls = true;
};

const hideVideoControls = () => {
  if (!state_video_controls.isMouseOverControls && (!ref_video.value || !ref_video.value.paused)) {
    state_video_controls.isShowControls = false;
  }
};

const handleMouseEnterControls = () => {
  state_video_controls.isMouseOverControls = true;
  showVideoControls();
};

const handleMouseLeaveControls = () => {
  state_video_controls.isMouseOverControls = false;
  hideVideoControls();
};
 
const handleMouseMove = () => {
  showVideoControls();
  clearTimeout(state_video_controls.mouseMoveTimeout);
  state_video_controls.mouseMoveTimeout = setTimeout(() => {
    hideVideoControls();
  }, 2000); 
};

// video player speed states

const resetPlaybackRate = () => {
  clearInterval(state_video_controls.fastForwardInterval);
  clearInterval(state_video_controls.fastBackwardInterval);
  state_video_controls.fastBackwardInterval = null;
  state_video_controls.fastForwardInterval = null;

  ref_video.value.playbackRate = 1; // Reset to normal speed
  state_video_controls.currentForwardSpeed = 1;
  state_video_controls.currentBackwardSpeed = 1; // Reset to normal playback
};

const activateBackwardSpeed = () => {
  clearInterval(state_video_controls.fastForwardInterval); 
  state_video_controls.fastForwardInterval = null;

  updateBackwardSpeed();

  if (state_video_controls.fastBackwardInterval) {
    clearInterval(state_video_controls.fastBackwardInterval); // Clear existing interval if any
  }

  state_video_controls.fastBackwardInterval = setInterval(() => {
    // Calculate new currentTime, ensuring it doesn't go below 0
    const newTime = Math.max(ref_video.value.currentTime - (1 / state_video_controls.currentBackwardSpeed), 0);
    ref_video.value.currentTime = newTime;
  }, 100); // Adjust as needed
};

const updateBackwardSpeed = () => {
  state_video_controls.currentForwardSpeed = 1; // Reset forward speed
  let nextIndex = (state_video_controls.avaiableBackwardSpeeds.indexOf(state_video_controls.currentBackwardSpeed) + 1) % state_video_controls.avaiableBackwardSpeeds.length;
  state_video_controls.currentBackwardSpeed = state_video_controls.avaiableBackwardSpeeds[nextIndex];
};

const activateForwardSpeed = () => { 
  clearInterval(state_video_controls.fastBackwardInterval);
  state_video_controls.fastBackwardInterval = null; 

  updateForwardSpeed();
  
  ref_video.value.playbackRate = state_video_controls.currentForwardSpeed; // Update playback rate
};

const updateForwardSpeed = () => {
  state_video_controls.currentBackwardSpeed = 1; // Reset backward speed
  let nextIndex = (state_video_controls.avaiableForwardSpeeds.indexOf(state_video_controls.currentForwardSpeed) + 1) % state_video_controls.avaiableForwardSpeeds.length;
  state_video_controls.currentForwardSpeed = state_video_controls.avaiableForwardSpeeds[nextIndex];
};

// Dragging video player controls state
const state_drag_video_controls = reactive({
  isDragging: false,
  startX: 0,
  startY: 0,
  offsetX: 0,
  offsetY: 0,
  initialPercentages: { left: 0, top: 0 }
}); 
 
// Dragging Controls Container
const startDragControlsContainer = (event) => { 
  if (event.target.tagName === 'BUTTON' 
    || event.target.tagName === 'INPUT' 
    || event.target.className === "progress-controls"
    || event.target.className === "media-controls"
    || event.target.className === "max-min-screen-button") {
    return;
  }
   
  state_drag_video_controls.isDragging = true;
  state_drag_video_controls.startX = event.clientX;
  state_drag_video_controls.startY = event.clientY;

  window.addEventListener('mousemove', draggingControlsContainer);
  window.addEventListener('mouseup', stopDragControlsContainer);
};

const stopDragControlsContainer = () => {   
  state_drag_video_controls.isDragging = false;
  const computedStyle = window.getComputedStyle(ref_video_controls.value);
  state_drag_video_controls.offsetX = parseFloat(computedStyle.left);
  state_drag_video_controls.offsetY = parseFloat(computedStyle.top);

  window.removeEventListener('mousemove', draggingControlsContainer);
  window.removeEventListener('mouseup', stopDragControlsContainer);
};

const draggingControlsContainer = (event) => {
  if (state_drag_video_controls.isDragging) {
    if (!ref_video.value || !ref_video_controls.value) {
      return; // Ensure elements are available
    }
    const dx = event.clientX - state_drag_video_controls.startX;
    const dy = event.clientY - state_drag_video_controls.startY;

    // Calculate new position
    let newX = state_drag_video_controls.offsetX + dx;
    let newY = state_drag_video_controls.offsetY + dy;
 

    // Constrain the new position within the video container
    const videoRect = ref_video.value.getBoundingClientRect();
    const controlRect = ref_video_controls.value.getBoundingClientRect();

    if (newX < 0) newX = 0;
    if (newY < 0) newY = 0;
    if (newX + controlRect.width > videoRect.width) newX = videoRect.width - controlRect.width;
    if (newY + controlRect.height > videoRect.height) newY = videoRect.height - controlRect.height;

    // Set the new position
    ref_video_controls.value.style.left = `${newX}px`;
    ref_video_controls.value.style.top = `${newY}px`;
  }
};

const updateInitialPercentages = () => {
  const videoRect = ref_video_container.value.getBoundingClientRect();
  const controlsRect = ref_video_controls.value.getBoundingClientRect();

  state_drag_video_controls.initialPercentages.left = (controlsRect.left - videoRect.left) / videoRect.width * 100;
  state_drag_video_controls.initialPercentages.top = (controlsRect.top - videoRect.top) / videoRect.height * 100;
};

const updatePositionOnResize = () => {
  const videoRect = ref_video_container.value.getBoundingClientRect();
  state_drag_video_controls.offsetX = (videoRect.width - ref_video_controls.value.getBoundingClientRect().width)/ 2;
  state_drag_video_controls.offsetY = videoRect.height * state_drag_video_controls.initialPercentages.top / 100;

  ref_video_controls.value.style.left = `${state_drag_video_controls.offsetX}px`;
  ref_video_controls.value.style.top = `${state_drag_video_controls.offsetY}px`;
};

onMounted(() => { 
  window.addEventListener('resize', updatePositionOnResize);
  document.addEventListener('keydown', handleHotKeys);
  
  state_video_controls.isShowControls = true;
  
  if (state_video.duration === 0 && ref_video.value && ref_video.value.paused) {
    ref_video.value.load(); // reload metadata
  }

  if (ref_video.value && ref_volume_slider.value) {
    ref_video.value.volume = state_video.volume;
    ref_volume_slider.value.value = state_video.volume;

    // Update the slider's visual progress
    // Call updateVolumeSlider with a simulated event object
    updateVolumeSlider({ target: { value: state_video.volume.toString() } });
  } else {
    // If the volume slider or video ref isn't available, log an error or handle appropriately
    console.error("Volume slider or video reference not available.");
  }

  // Update position based on computed styles
  if (ref_video_controls.value) {
    const computedStyle = window.getComputedStyle(ref_video_controls.value);
    state_drag_video_controls.offsetX = parseFloat(computedStyle.left);
    state_drag_video_controls.offsetY = parseFloat(computedStyle.top);
    ref_video_controls.value.style.left = `${state_drag_video_controls.offsetX}px`;
    ref_video_controls.value.style.top = `${state_drag_video_controls.offsetY}px`;

    updateInitialPercentages();
  } else {
    console.error("Video controls reference not available.");
  }
}); 

onUnmounted(() => {
  window.removeEventListener('resize', updatePositionOnResize);
});
 
const updateVolumeSliderVisualOnHotKey = (newVolume) => {
  // Assuming state_video and ref_volume_slider are defined and accessible
  state_video.volume = newVolume;
  if (ref_volume_slider.value) {
    ref_volume_slider.value.value = newVolume;
    updateVolumeSlider({ target: { value: newVolume.toString() } });
  }
}

const updateVideoProgressOnHotKey  = () => {
  if (ref_video.value && ref_progress_slider.value) {
    state_video.progress = ref_video.value.currentTime;
    updateVideoSliderProgress();
  }
}

// hotkeys 
const handleHotKeys = (event) => {
  switch (event.code) {
        case 'Space': // Toggle play/pause
          toggleMediaPlayPause();
          event.preventDefault();
          break; 
        case 'KeyM': // Toggle mute
          toggleMute();
          event.preventDefault();
          break;
        case 'ArrowLeft':  
          if (ref_video.value) {
            let newTime = Math.max(ref_video.value.currentTime - 5, 0); // Seek backward 5 seconds, but not less than 0
            ref_video.value.currentTime = newTime;
            updateVideoProgressOnHotKey();
          }
          event.preventDefault();
          break;
        case 'ArrowRight':  
          if (ref_video.value) {
            let newTime = Math.min(ref_video.value.currentTime + 5, ref_video.value.duration); // Seek forward 5 seconds, but not beyond duration
            ref_video.value.currentTime = newTime;
            updateVideoProgressOnHotKey();
          }
          break;
        case 'ArrowUp': // Increase volume
          if (ref_video.value) {
            let newVolume = Math.min(ref_video.value.volume + 0.1, 1); // Increase volume, max 1
            ref_video.value.volume = newVolume;
            updateVolumeSliderVisualOnHotKey(newVolume);
          }
          event.preventDefault();
          break;
        case 'ArrowDown': // Decrease volume
          if (ref_video.value) {
            let newVolume = Math.max(ref_video.value.volume - 0.1, 0); // Decrease volume, min 0
            ref_video.value.volume = newVolume;
            updateVolumeSliderVisualOnHotKey(newVolume);
          }
          event.preventDefault();
          break;
        case 'KeyF': // Toggle fullscreen
          toggleFullScreen();
          event.preventDefault();
          break; 
        default:
          // Handle number keys for skipping
          if (event.code.startsWith('Digit') || event.code.startsWith('Numpad')) {
            const percentage = parseInt(event.code.substr(-1));
            if (!isNaN(percentage)) {
              if (ref_video.value) {
                // Calculate new time based on percentage
                const newTime = (percentage / 10) * ref_video.value.duration;
                ref_video.value.currentTime = newTime;
                // Update the video progress
                state_video.progress = newTime;
                updateVideoSliderProgress();
              }
              event.preventDefault();
            }
          }
    }
}
</script> 

<script> 
  import MediaPauseIcon from "@/components/video/icons/media-pause.vue";
  import MediaPlayIcon from "@/components/video/icons/media-play.vue";
  import mediaFastForwardIcon from "@/components/video/icons/media-fast-forward.vue";
  import mediaFastBackwardIcon from "@/components/video/icons/media-fast-backward.vue";
  import mediaMaximizeIcon from "@/components/video/icons/media-maximize.vue";
  import mediaMinimizeIcon from "@/components/video/icons/media-minimize.vue";
  import mediaOptionsIcon from "@/components/video/icons/media-options.vue";
  import mediaVolumeIcon_0 from "@/components/video/icons/media-volume-0.vue";
  import mediaVolumeIcon_1 from "@/components/video/icons/media-volume-1.vue";
  import mediaVolumeIcon_2 from "@/components/video/icons/media-volume-2.vue";
  import mediaVolumeIcon_3 from "@/components/video/icons/media-volume-3.vue";
  import MediaFastBackwardIcon from "@/components/video/icons/media-fast-backward.vue";

  export default {
    components: {
      MediaPauseIcon,
      MediaPlayIcon,
      mediaFastForwardIcon,
      mediaFastBackwardIcon,
      mediaMaximizeIcon,
      mediaMinimizeIcon,
      mediaOptionsIcon,
      mediaVolumeIcon_0,
      mediaVolumeIcon_1,
      mediaVolumeIcon_2,
      mediaVolumeIcon_3,
      MediaFastBackwardIcon
    },
    props: {
      src: String,
      type: {
        type: String,
        default: 'video/mp4'
      },
      height: {
        type: String,
        default: '100vh'
      },
      width: {
        type: String,
        default: '100vw'
      }
    },  
  };
</script> 


<template>
  <section 
    ref="ref_video_container" 
    class="video-container"
    @mousemove="handleMouseMove">
      <video 
        ref="ref_video" 
        :style="{ width: width, height: height, zIndex: 0}" 
        @timeupdate="handleVideoTimeUpdate" 
        @loadedmetadata="handleVideoMetadata" 
        @waiting="onVideoWaiting" 
        @canplay="onVideoCanPlay" 
        @play="state_video.isPlaying = true" 
        @pause="state_video.isPlaying = false"
        @click="toggleMediaPlayPause">
        <source :src="src" :type="type">
        <p>Your browser does not support the video tag.</p> 
      </video> 
      <div 
        v-if="state_video.isLoading" 
        class="video-loading-overlay"
        style="z-index: 1"
      ></div>
      <section 
        ref="ref_video_controls" 
        class="video-controls-container"
        @mousedown="startDragControlsContainer"
        @mouseup="stopDragControlsContainer" 
        @mousemove="draggingControlsContainer"
        @mouseenter="handleMouseEnterControls" 
        @mouseleave="handleMouseLeaveControls"
        :style="{ visibility: state_video_controls.isShowControls ? 'visible' : 'hidden' , zIndex: 2}"
        >
        <section class="video-controls-wrapper">
          <section class="video-controls">
            <section class="volume-controls" 
                @mouseleave="handleMouseLeaveVolumeControls"
              >
              <button 
                class="volume-button"
                @click="toggleMute"
                @mouseenter="handleMouseEnterVolumeControls"
                >
                <media-volume-icon_0
                  v-if="state_video.volume === 0 || state_video.isMuted"
                  class="icon-color"
                  style="scale: 0.8;"/>
                <media-volume-icon_1 
                  v-else-if="state_video.volume > 0 && state_video.volume <= 0.33"
                  class="icon-color"
                  style="scale: 0.8;"/>
                <media-volume-icon_2 
                  v-else-if="state_video.volume > 0.33 && state_video.volume <= 0.66"
                  class="icon-color"
                  style="scale: 0.8;"/>
                <media-volume-icon_3 
                  v-else
                  class="icon-color"
                  style="scale: 0.8;"/>
              </button>
              <span class="volume-tooltip" ref="ref_volume_tool_tip">{{ `${Math.round(state_video.volume * 100)}%` }}</span>
              <input 
                type="range" 
                class="volume-slider"
                ref="ref_volume_slider"
                min="0" 
                max="1" 
                step="0.01"
                @input="updateVolumeSlider($event)" 
                @mousedown="handleRangeSliderMouseDown"
                @mouseup="handleRangeSliderMouseUp"
                >
            </section>
            
            <section class="media-controls">
              <button 
                class="fast-backward-button"
                @click="activateBackwardSpeed" >
                <span class="fast-backward-span"
                  :style="{visibility: state_video_controls.currentBackwardSpeed > 1 ? 'visible' : 'hidden' }">
                  {{ state_video_controls.currentBackwardSpeed }}x
                </span>
                <media-fast-backward-icon 
                  class="icon-color"
                  :style="`scale: ${1}; margin-right: 1rem;`"
                  />
              </button>
              <button class="toggle-media-play-pause-button"
                @click="toggleMediaPlayPause"
                >
                <media-play-icon 
                  v-if="!state_video.isPlaying" 
                  class="icon-color"
                  :style="`scale: 2; transform: translateX(-1.5px); margin: auto;`" />
                <media-pause-icon 
                  v-else 
                  class="icon-color"
                  :style="`scale: 2; margin: auto;`" />
              </button>
              <button class="fast-forward-button"
                @click="activateForwardSpeed" >
                <media-fast-forward-icon 
                  class="icon-color"
                  :style="`scale: ${1}; margin-left: 1rem;`"
                />
                <span class="fast-forward-span" :style="{ visibility: state_video_controls.currentForwardSpeed > 1 ? 'visible' : 'hidden' } ">
                  {{ state_video_controls.currentForwardSpeed }}x
                </span>
              </button>
            </section>

            <section class="additional-controls">
              <button class="max-min-screen-button"
                @click="toggleFullScreen">
                <media-maximize-icon  
                  v-if="!state_video_controls.isFullscreen"
                  class="icon-color"
                  style="scale: 0.8;"
                  />
                <media-minimize-icon   
                  v-else
                  class="icon-color"
                  style="scale: 0.8;"
                  />
              </button>
              <!--  
              <button class="options-button" > 
                  <media-options-icon
                    class="icon-color"
                    style="scale: 0.8; margin-left: 1.5rem;"
                  />
              </button>
              --> 
            </section>
          </section>
          <section class="progress-controls">
            <span class="video-current-time">
              {{ formatTime(state_video.progress) }}
            </span>
            <section class="video-progress-slider-wrapper">
              <input 
                type="range" 
                class="video-progress-slider"
                :class="{ 'loading': state_video.isLoading }"
                ref="ref_progress_slider"
                min="0"
                :max="state_video.duration" 
                :value="state_video.progress"
                @input="onVideoProgressSliderInput($event)"
                @mousedown="handleRangeSliderMouseDown"
                @mouseup="handleRangeSliderMouseUp"
              >
              <div 
                v-if="state_video.isLoading" 
                class="loading-overlay" 
                :style="{ width: calculateProgressSliderLoadingWidth() + '%' }">
              </div>
            </section>
            <span class="video-duration-time">
              {{formatTime(state_video.duration) }}
            </span>
          </section>
        </section>
      </section>
  </section>
</template>

<style scoped>

.loading-overlay {
  position: absolute;
  top: 0;
  right: 0;
  height: 100%;
  background: repeating-linear-gradient(    
    -45deg,    
    #dedede,    
    #dedede 10px,    
    #a3a2a2 10px,    
    #a3a2a2 20px  );
  background-size: 200% 100%;
  animation: moveHorizontal 10s linear infinite;
  border-radius: 5px;
  pointer-events: none;
}

@keyframes moveHorizontal {
  from { background-position: 100% 0; }
  to { background-position: 0% 0; }
}

.video-loading-overlay{
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5); /* Semi-transparent black */
}
/* Add styles for your .video-progress-slider as needed */

.video-container{
  position: relative;
  background-color: rgb(0, 0, 0);
}

/* Video Controls */
.video-controls-container{
  position: absolute;  
  left: calc((100vw - 440px)/2);
  top: 85%;
}

.video-controls-wrapper {  
  /* Glass Like Background */
  position: relative;
  background: inherit;
  overflow: hidden; 
  margin: auto;  
  width: 440px;
  max-width: 100%; 
  height: 70%;
  border-radius: 0.5rem;
  background: rgb(0 0 0 / 40%);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3), 
              0 6px 20px rgba(0, 0, 0, 0.15);
  backdrop-filter: blur(10px);
  z-index: 1;
  padding: 0.5rem;
}

.video-controls-wrapper:before {
  content: '';
  position: absolute;
  background: inherit;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  margin: -20px;
  box-shadow: inset 0 0 500px rgb(160 160 160 / 40%); 
  filter: blur(10px);
  z-index: -1;
}

@media (max-width: 450px) {
  .video-controls-wrapper{
    width: 90vw;
  }  
}

@media (max-width: 440px) { 
  .options-button{
    margin-left: 0px !important;
  }
  .fast-forward-button, .fast-backward-button{
    display: none !important;
  }
}

.video-controls{
  align-items: center;
  justify-content: space-between;
  width: 100%;
  color: #9a9a9a;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
}

/* -- -- -- */
.icon-color{
  color: white;
}

/* Media Controls */

.media-controls{
  display: flex;
  justify-content: center;
  flex-grow: 1; 
}

.volume-controls{
  display: flex;     
  align-items: center;
}

.volume-button{
  width: 22px;
  height: 44px;
}

.volume-slider{
  display: none;
  margin-left: 0.6rem;
}

.volume-tooltip {
  position: absolute;
  margin-bottom: 2rem;
  font-size: 0.7rem;
  transform: translateX(150%);
  display: none; 
}

.fast-backward-button, .fast-forward-button{
  display: inline-flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
}

.fast-backward-span, .fast-forward-span{
  font-size: 0.8rem;
  width: 22px;
}

.toggle-media-play-pause-button{
  width: 44px; 
  height: 44px;
}

.additional-controls{
  display: flex; 
  justify-content: flex-end;
}

.max-min-screen-button, .options-button{
  display: flex;
  justify-content: center;
  align-items: center;
}
.max-min-screen-button{ 
  height: 44px;
  width: 44px; 
}
.options-button {
  width: 22px;
  margin-left: 1rem;
}

/* Progress Controls */
.progress-controls{
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

.video-current-time, .video-duration-time{
  color: #9a9a9a;
  flex: 0 0 auto;
  width: 40px;      
  font-size: 0.8rem;
  text-align: center;
}

.video-current-time{
  text-align: left;
}

.video-duration-time{
  text-align: right;
}

.video-progress-slider-wrapper{
  width: 100%;
  display: flex;
  align-items: center;
  position: relative;
}

.video-progress-slider ,
.volume-slider {
  appearance: none;
  -webkit-appearance: none;
  width: 100%;
  background:  rgba(154, 154, 154, 40%);
  height: 0.225rem;
  border-radius: 5px;
  position: relative;
  z-index: 2;
}

.video-progress-slider::before,
.volume-slider::before {
  content: '';
  position: absolute;
  left: 0;
  height: 0.225rem;
  border-radius: 5px;
  width: 100%;
  z-index: 1;
}

.video-progress-slider::before {
  background: linear-gradient(to right, rgba(196, 196, 196, 0.4) 0%, rgba(196, 196, 196, 0.4) var(--video-slider-progress, 0%), transparent  var(--video-slider-progress, 0%));
}

.volume-slider::before { 
  background: linear-gradient(to right, rgba(196, 196, 196, 0.4) 0%, rgba(196, 196, 196, 0.4) var(--volume-slider-progress, 0%), transparent  var(--volume-slider-progress, 0%));
} 

.slider-active,
.slider-active::before {
  height: 0.30rem; /* Increased height during mouse down */
}

/* Ensure the pseudo-element tracks the slider's height */
.video-progress-slider.slider-active::before,
.volume-slider.slider-active::before {
  height: inherit;
}

.video-progress-slider::-webkit-slider-thumb,
.volume-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 4px;
  height: 0.55rem;
  border-radius: 1rem;
  background:  white; 
  cursor: pointer;
}
 
.video-progress-slider::-webkit-slider-runnable-track 
.volume-slider::-webkit-slider-runnable-track  {
  background: #666;
  border-radius: 5px;
  height: 5px; 
} 
 
.video-progress-slider::-moz-range-track, 
.volume-slider::-moz-range-track {
  background: #666;
  border-radius: 5px;
  height: 0.55rem;
} 
 
.volume-slider::-moz-range-thumb,
.video-progress-slider::-moz-range-thumb{
  width: 8px;
  height: 20px;
  background: #fff;
  cursor: pointer; 
} 
</style>