PREFIX := .compiled

.PHONY = all clean xclip pbcopy

all: game.hex

#$(PREFIX)/heads.8o: Makefile assets/heads/* generate-texture.py
#		./generate-texture.py assets/heads/kesha_v2.png kesha 2 16 > $@
#		./generate-texture.py assets/heads/kesha_v2_open.png kesha_o 2 16 >> $@
#		./generate-texture.py assets/heads/kesha_v2_excited.png kesha_e 2 16 >> $@
#		./generate-texture.py assets/heads/squirrel_2.png cow 2 16 >> $@
#		./generate-texture.py assets/heads/professor.png professor_old 2 16 >> $@
#		./generate-texture.py assets/heads/professor2.png professor 2 16 >> $@
#		./generate-texture.py assets/heads/ninja.png ninja_old 2 16 >> $@
#		./generate-texture.py assets/heads/ninja2.png ninja 2 16 >> $@
#		./generate-texture.py assets/heads/ninja_kesha.png ninja_kesha 2 16 >> $@
#		./generate-texture.py assets/heads/lab.png lab 2 16 >> $@
#		./generate-texture.py assets/heads/disabled.png disabled 2 16 >> $@
#		./generate-texture.py assets/heads/fish.png fish 2 16 >> $@
#		./generate-texture.py assets/heads/pets2.png pets 2 16 >> $@
#
$(PREFIX)/dtmf.8o: Makefile ./generate-dtmf.py
		./generate-dtmf.py > $@

$(PREFIX)/music_eb4.8o: Makefile ./generate-keys.py
		./generate-keys.py > $@

#$(PREFIX)/banners.8o: Makefile ./generate-texture.py assets/big_pics/*
#		./generate-texture.py assets/big_pics/drinking.png drinking 2 16 > $@
#		./generate-texture.py assets/big_pics/fday_devise.png banner_fday_device 2 16 >> $@
#		./generate-texture.py assets/big_pics/fish.png banner_fish 2 16 >> $@
#		./generate-texture.py assets/big_pics/galina.png banner_galina 2 16 >> $@
#		./generate-texture.py assets/big_pics/galina_pests.png banner_galina_pests 2 16 >> $@
#		./generate-texture.py assets/big_pics/memory_erizer.png banner_memory_eraser 2 16 >> $@
#		./generate-texture.py assets/big_pics/ninja.png banner_ninja 2 16 >> $@
#		./generate-texture.py assets/big_pics/phone_notepad.png phone_screen 2 16 >> $@
#		./generate-texture.py assets/big_pics/prison.png banner_prison 2 16 >> $@
#		./generate-texture.py assets/big_pics/professor.png banner_professor 2 16 >> $@
#		./generate-texture.py assets/big_pics/ninja_fish.png ninja_fish 2 16 >> $@
#		./generate-texture.py assets/big_pics/ninja_kills_kesha.png ninja_kills_kesha 2 16 >> $@
#		./generate-texture.py assets/big_pics/ninja_kills_kesha_2.png ninja_kills_kesha_2 2 16 >> $@
#		./generate-texture.py assets/big_pics/ninja_kills_kesha_3.png ninja_kills_kesha_3 2 16 >> $@
#		./generate-texture.py assets/big_pics/fish_army.png fish_army 2 16 >> $@
#		./generate-texture.py assets/big_pics/earth.png earth_1 2 16 >> $@
#		./generate-texture.py assets/big_pics/earth_2.png earth_2 2 16 >> $@
#		./generate-texture.py assets/big_pics/earth_3.png earth_3 2 16 >> $@
#		./generate-texture.py assets/big_pics/earth_4.png earth_4 2 16 >> $@

$(PREFIX)/tiles.8o: Makefile ./generate-texture.py assets/tiles/* #assets/*.png
		./generate-texture.py assets/tiles/splash.png splash 2 16 > $@
#		./generate-texture.py assets/frame.png frame 2 16 >> $@
#		./generate-texture.py assets/room.png room 2 16 >> $@

$(PREFIX)/dialogs.8o $(PREFIX)/dialogs.json: Makefile generate-dialogs.py pykesha/dialogs.py
		./generate-dialogs.py $(PREFIX)

$(PREFIX)/font.8o $(PREFIX)/font-data.8o: Makefile generate-font.py assets/font/5.font
		./generate-font.py assets/font/5.font font 1000 $(PREFIX)

$(PREFIX)/map.8o $(PREFIX)/map.json: Makefile generate-map.py pykesha/map.py
		./generate-map.py $(PREFIX)

$(PREFIX)/texts.8o $(PREFIX)/texts_data.8o: Makefile assets/en.json $(PREFIX)/map.json generate-text.py
		./generate-text.py $(PREFIX) 1500 assets/en.json $(PREFIX)/map.json

$(PREFIX)/audio.8o: Makefile ./generate-audio.py assets/sounds/*
		./generate-audio.py assets/sounds/kesha.wav 8000 -c -0.3 music > $@

$(PREFIX)/signature.8o: Makefile ./generate-string.py
		./generate-string.py --right-align=60000 "Brought to you by Gazay & Whoozle. FROM LOVE WITH COW ©7524" > $@

game.8o: Makefile $(PREFIX)/texts.8o \
$(PREFIX)/texts_data.8o $(PREFIX)/font.8o $(PREFIX)/dialogs.8o \
$(PREFIX)/dtmf.8o $(PREFIX)/audio.8o $(PREFIX)/signature.8o \
$(PREFIX)/tiles.8o sources/map_runtime.8o $(PREFIX)/map.8o \
$(PREFIX)/music_eb4.8o \
assets/* assets/*/* sources/*.8o generate-texture.py
		cat sources/main.8o > $@
		cat $(PREFIX)/texts.8o >> $@
		cat $(PREFIX)/font.8o >> $@
		cat sources/map_runtime.8o >> $@
		cat $(PREFIX)/map.8o >> $@
		cat sources/flags.8o >> $@
		cat sources/intro.8o >> $@
#		cat $(PREFIX)/dialogs.8o >> $@
		cat sources/utils.8o >> $@
		cat sources/text.8o >> $@
		cat sources/tiles.8o >> $@
		cat sources/splash.8o >> $@
		cat sources/audio.8o >> $@
		cat $(PREFIX)/font_data.8o >> $@
		cat $(PREFIX)/texts_data.8o >> $@
		cat sources/audio_data.8o >> $@
		cat $(PREFIX)/music_eb4.8o >> $@
		cat $(PREFIX)/tiles.8o >> $@
#		cat $(PREFIX)/heads.8o >> $@
		cat $(PREFIX)/dtmf.8o >> $@
#		cat $(PREFIX)/banners.8o >> $@
		cat $(PREFIX)/audio.8o >> $@
#		cat $(PREFIX)/signature.8o >> $@

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
