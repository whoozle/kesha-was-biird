PREFIX := .compiled

.PHONY = all clean xclip pbcopy

all: game.hex

#$(PREFIX)/dtmf.8o: Makefile ./generate-dtmf.py
#		./generate-dtmf.py > $@

$(PREFIX)/music_eb4.8o: Makefile ./generate-keys.py
		./generate-keys.py > $@

$(PREFIX)/tiles.8o: Makefile ./generate-texture.py assets/tiles/* #assets/*.png
		./generate-texture.py assets/tiles/splash.png splash 2 16 > $@
#		./generate-texture.py assets/tiles/frame.png frame 2 16 >> $@
		./generate-texture.py assets/tiles/room.png room 2 16 >> $@
		./generate-texture.py assets/tiles/dream.png dream 2 16 >> $@
		./generate-texture.py assets/tiles/chav.png chav 2 16 >> $@
		./generate-texture.py assets/tiles/galina-on-balcony.png galina 2 16 >> $@
		./generate-texture.py assets/tiles/heads/professor.png professor 2 16 >> $@
		./generate-texture.py assets/tiles/heads/fish.png fish 2 16 >> $@
		./generate-texture.py assets/tiles/tm_empty.png time_machine 2 16 >> $@
		./generate-texture.py assets/tiles/tm_empty_banner.png time_machine_banner 2 16 >> $@
		./generate-texture.py assets/tiles/tm_w_fish.png time_machine_fish 2 16 >> $@
		./generate-texture.py assets/tiles/tm_w_nuke.png time_machine_isotope 2 16 >> $@
		./generate-texture.py assets/tiles/tm_w_nuke_and_fish.png time_machine_fish_isotope 2 16 >> $@
		./generate-texture.py assets/tiles/dead_ninja.png dead_ninja 2 16 >> $@
		./generate-texture.py assets/tiles/professor-cage.png chapter1 2 16 >> $@
		./generate-texture.py assets/tiles/city.png chapter2 2 16 >> $@
		./generate-texture.py assets/tiles/chip9.png chapter3 2 16 >> $@


$(PREFIX)/dialogs.8o $(PREFIX)/dialogs.json: Makefile generate-dialogs.py pykesha/dialogs.py
		./generate-dialogs.py $(PREFIX)

$(PREFIX)/font.8o $(PREFIX)/font-data.8o: Makefile generate-font.py assets/font/5.font
		./generate-font.py assets/font/5.font font 1100 $(PREFIX)

$(PREFIX)/chapter1.8o $(PREFIX)/chapter1.json: Makefile generate-chapter1.py pykesha/map.py
		./generate-chapter1.py $(PREFIX)
$(PREFIX)/chapter2.8o $(PREFIX)/chapter2.json: Makefile generate-chapter2.py pykesha/map.py
		./generate-chapter2.py $(PREFIX)
$(PREFIX)/chapter3.8o $(PREFIX)/chapter3.json: Makefile generate-chapter3.py pykesha/map.py
		./generate-chapter3.py $(PREFIX)

$(PREFIX)/texts.8o $(PREFIX)/texts_data.8o: Makefile assets/en.json $(PREFIX)/dialogs.json \
$(PREFIX)/chapter1.json $(PREFIX)/chapter2.json $(PREFIX)/chapter3.json \
generate-text.py
		./generate-text.py $(PREFIX) 1600 assets/en.json \
		$(PREFIX)/chapter1.json $(PREFIX)/chapter2.json $(PREFIX)/chapter3.json $(PREFIX)/dialogs.json

$(PREFIX)/audio.8o: Makefile ./generate-audio.py assets/sounds/*
		./generate-audio.py assets/sounds/kesha.wav a100 music -c 0.25 -l4 -o $(PREFIX)/audio.wav > $@

$(PREFIX)/signature.8o: Makefile ./generate-string.py
		./generate-string.py --right-align=65000 "BROUGHT TO YOU BY WHOOZLE, GAZAY & FOGGY. FROM LOVE WITH COW AND THANKS FOR ALL THE FISH. FISH! FISH! YOU GOT IT?? GOT IT??? FISH!!! AHAHAHAHAHAHA ©7524" > $@

game.8o: Makefile $(PREFIX)/texts.8o \
$(PREFIX)/texts_data.8o $(PREFIX)/font.8o $(PREFIX)/dialogs.8o \
$(PREFIX)/audio.8o $(PREFIX)/signature.8o \
$(PREFIX)/tiles.8o sources/map_runtime.8o $(PREFIX)/dialogs.8o \
$(PREFIX)/chapter1.8o $(PREFIX)/chapter2.8o $(PREFIX)/chapter3.8o \
$(PREFIX)/music_eb4.8o \
assets/* assets/*/* sources/*.8o generate-texture.py
		cat sources/main.8o > $@
		cat $(PREFIX)/texts.8o >> $@
		cat $(PREFIX)/font.8o >> $@
		cat sources/map_runtime.8o >> $@
		cat sources/flags.8o >> $@
		cat $(PREFIX)/chapter1.8o >> $@
		cat $(PREFIX)/chapter2.8o >> $@
		cat $(PREFIX)/chapter3.8o >> $@
		cat sources/music.8o >> $@
		cat sources/intro.8o >> $@
		cat sources/outro.8o >> $@
		cat sources/prologue.8o >> $@
		cat sources/chapter.8o >> $@
		cat $(PREFIX)/dialogs.8o >> $@
		cat $(PREFIX)/music_eb4.8o >> $@
		cat sources/utils.8o >> $@
		cat sources/text.8o >> $@
		cat sources/tiles.8o >> $@
		cat sources/splash.8o >> $@
		cat sources/audio.8o >> $@
		cat $(PREFIX)/font_data.8o >> $@
		cat $(PREFIX)/texts_data.8o >> $@
		cat sources/audio_data.8o >> $@
		cat $(PREFIX)/tiles.8o >> $@
#		cat $(PREFIX)/heads.8o >> $@
#		cat $(PREFIX)/dtmf.8o >> $@
#		cat $(PREFIX)/banners.8o >> $@
		cat $(PREFIX)/audio.8o >> $@
		cat $(PREFIX)/signature.8o >> $@

game.bin: game.8o
	./octo/octo game.8o $@

game.hex: game.bin ./generate-hex.py
	./generate-hex.py game.bin $@

xclip: game.hex
	cat game.hex | xclip

pbcopy: game.hex
	cat game.hex | pbcopy

clean:
		rm -f game.bin game.8o game.hex .compiled/*
