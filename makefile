
all: icons

# -----------------------------------------------------------------------------
# MARK: Icons
# -----------------------------------------------------------------------------

# the path to the logo PNG
LOGO=uhue/static/img/logo.png
# the path to the favicon
FAVICON=uhue/static/favicon.ico

# create the Favicon from the logo PNG
icon_favicon:
	convert ${LOGO} -background white \
	          \( -clone 0 -resize 16x16 -extent 16x16 \) \
	          \( -clone 0 -resize 32x32 -extent 32x32 \) \
	          \( -clone 0 -resize 48x48 -extent 48x48 \) \
	          \( -clone 0 -resize 64x64 -extent 64x64 \) \
	          -delete 0 -alpha off -colors 256 ${FAVICON}

# the directory for icons
ICONS=uhue/static/img
# the Android 192 icon file name
ANDROID192=${ICONS}/android-chrome-192x192.png

icon_android192:
	convert ${LOGO} -background transparent \
	          \( -clone 0 -resize 192x192 -extent 192x192 \) \
	          -delete 0 -alpha on -colors 256 ${ANDROID192}

# the Android 512 icon file name
ANDROID512=${ICONS}/android-chrome-512x512.png

icon_android512:
	convert ${LOGO} -background transparent \
	          \( -clone 0 -resize 512x512 -extent 512x512 \) \
	          -delete 0 -alpha on -colors 256 ${ANDROID512}

# the Apple Touch icon file name
APPLE_TOUCH=${ICONS}/apple-touch-icon.png

icon_apple_touch:
	convert ${LOGO} -background transparent \
	          \( -clone 0 -resize 180x180 -extent 180x180 \) \
	          -delete 0 -alpha on -colors 256 ${APPLE_TOUCH}

# create all the icons
icons: icon_favicon icon_android192 icon_android512 icon_apple_touch
