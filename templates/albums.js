var audioElem = document.createElement('audio');
audioElem.controls = false;
audioElem.preload = "none";

var canPlayAudio = (audioElem.play)? true : false;
if(canPlayAudio) {
	var albums = {{ album_json|safe }};
	var playIcon = document.getElementById('play-icon');
	var playLinks = document.querySelectorAll('a[data-album]');
	var mpegSource = document.createElement('source');
	var oggSource = document.createElement('source');
	var volumeControl = document.getElementById('vol-control');
	var volIcon = document.getElementById('vol-icon');
	var stepBackwardIcon = document.getElementById('step-backward-icon');
	var stepForwardIcon = document.getElementById('step-forward-icon');
	var metaData = document.getElementById('meta');
	oggSource.type = "audio/ogg";
	mpegSource.type = "audio/mpeg";

	var setAudioSource = function(album,track) {
		album = album || albums.length - 1;
		track = track || 0;
		playIcon.dataset.album = album;
		playIcon.dataset.track = track;
		audioElem.dataset.album = album;
		audioElem.dataset.track = track;
		oggSource.src = "/audio/ogg/" + album + "/" + track;
		mpegSource.src = "/audio/mp3/" + album + "/" + track;
	}

	setAudioSource();
	audioElem.appendChild(oggSource);
	audioElem.appendChild(mpegSource);

	var getMetadata = function(a, t) {
		var albumTitle = albums[a].title;
		var albumArtist = albums[a].artist;
		var year = albums[a].year;
		var trackTitle = albums[a].tracks[t];
		return albumArtist + " -  " + trackTitle + " -  " + albumTitle + " (" + year + ")";
	}
	
	var controls = document.getElementById('audio-controls');
	controls.appendChild(audioElem);
	controls.style.visibility = 'visible';

	function getElementByAlbumAndTrack(album,track) {
		var elem = document.querySelector('li a[data-album="' + album + '"][data-track="' + track + '"]');
		return elem;
	}

	var updatePlayIcon = function() {
		var album = audioElem.dataset.album;
		var track = audioElem.dataset.track;
		var elem = getElementByAlbumAndTrack(album,track);
		if ( audioElem.paused ) {
			playIcon.innerHTML = 'play_arrow';
			elem.innerHTML = 'play_arrow';
			elem.className = 'material-icons text-muted';
		} else {
			playIcon.innerHTML = 'pause';
			elem.innerHTML = 'pause';
			elem.className = 'text-white material-icons';
		}
		var meta = getMetadata(album, track);
		metaData.innerHTML = meta;
		document.title = meta;
	};
	audioElem.addEventListener('ended',updatePlayIcon);
	audioElem.addEventListener('pause',updatePlayIcon);
	audioElem.addEventListener('playing',updatePlayIcon);

	var setVolume = function() {
		audioElem.volume = this.value / 100;
	};
	volumeControl.value = audioElem.volume * 100;
	volumeControl.addEventListener('change', setVolume);
	volumeControl.addEventListener('input', setVolume);

	var toggleMute = function() {
		var volIcon = document.getElementById('vol-icon');
		if ( audioElem.muted ) {
			volIcon.innerHTML = "volume_up";
			audioElem.muted = false;
		} else {
			volIcon.innerHTML = "volume_off";
			audioElem.muted = true;
		}
	};
	volIcon.addEventListener('click',toggleMute);

	var playTrack = function(album,track) {
			audioElem.pause();
			// for some reason, this pause doesn't trigger the event listener, so I have to explicitly call updatePlayIcon().
			updatePlayIcon();
			setAudioSource(album,track);
			audioElem.load();
			audioElem.play();
	}

	var togglePlayPause = function() {
		var trackToPlay = this.dataset.album + this.dataset.track;
		var trackPlaying = audioElem.dataset.album + audioElem.dataset.track;

		if (trackToPlay == trackPlaying) {
			if (audioElem.paused) {
				audioElem.play();
			} else {
				audioElem.pause();
			}
		} else {
			playTrack(this.dataset.album, this.dataset.track);
		}
	}

	for (var i=0; i < playLinks.length; i++) {
		playLinks[i].className = 'text-muted material-icons';
		playLinks[i].innerHTML = 'play_arrow';
		playLinks[i].addEventListener('click', togglePlayPause);
	}

	playIcon.addEventListener('click', togglePlayPause);

	var stepForward = function() {
		var a = parseInt(audioElem.dataset.album);
		var t = parseInt(audioElem.dataset.track);
		if ( albums[a].tracks[t+1] ) {
			playTrack(a, t+1);
		} else if ( albums[a-1] ) {
			playTrack(a-1, 0);
		} else {
			playTrack(albums.length - 1,0);
		}
	}
	stepForwardIcon.addEventListener('click',stepForward);
	audioElem.addEventListener('ended',stepForward);

	var stepBackward = function() {
		var a = parseInt(audioElem.dataset.album);
		var t = parseInt(audioElem.dataset.track);
		if ( albums[a].tracks[t-1] ) {
			playTrack(a, t-1);
		} else if ( albums[a+1] ) {
			playTrack(a+1, 0);
		} else {
			playTrack(0,albums.length - 1);
		}
	}
	stepBackwardIcon.addEventListener('click',stepBackward);

	if ( window.location.hash ) {
		var hash = window.location.hash.substring(1);
		if ( hash == 'autoplay' ) {
			playTrack(albums.length - 1,0);
		}
	}


}
