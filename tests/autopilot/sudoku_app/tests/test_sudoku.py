# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
# Copyright 2013 Canonical
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.

"""Sudoku app autopilot tests."""

from autopilot.matchers import Eventually
from testtools.matchers import Equals, NotEquals

from sudoku_app.tests import SudokuTestCase


class TestMainWindow(SudokuTestCase):

    def setUp(self):
        super(TestMainWindow, self).setUp()
        self.assertThat(
            self.main_view.visible, Eventually(Equals(True)))

    def test_enter_and_clear_number(self):
        # find the first button that has a blank value
        gridButtons = self.main_view.get_blank_inputs()
        gridButton = gridButtons[0]

        # create a value function to check later using id
        buttonValue = lambda: self.main_view.select_single(
            "QQuickText", id=gridButton.id).text

        # double check that it's blank
        self.assertThat(buttonValue, Eventually(Equals("")))

        # click the button
        self.pointing_device.click_object(gridButton)

        # assert that we can see the input screen
        self.main_view.get_number_dialog()

        # set a value, choose 4
        dialogButton = self.main_view.get_dialog_button("4")
        self.pointing_device.click_object(dialogButton)

        # check the value to ensure it worked
        self.assertThat(buttonValue, Eventually(Equals("4")))

        # click the button
        self.pointing_device.click_object(gridButton)

        # make sure we can see the input screen
        self.main_view.get_number_dialog()

        # set a value, choose clear
        dialogButton = self.main_view.get_dialog_button("Clear")
        self.pointing_device.click_object(dialogButton)

        # check the value to ensure it worked
        self.assertThat(buttonValue, Eventually(Equals("")))

    def test_best_scores_tab(self):
        # switch to best scores tab
        self.main_view.switch_to_tab("highscoresTab")

        # make sure we are in the right place
        self.main_view.wait_select_single("Tab", objectName="highscoresTab")

        # click current user button
        header = self.main_view.get_header()
        header.click_action_button('currentuserbutton')

        # check label
        label = lambda: self.main_view.wait_select_single(
            "Header", objectName="highscoreslabel").text
        self.assertThat(
            label,
            Eventually(NotEquals("<b>Best scores for all players</b>")))

        # click all users button
        header = self.main_view.get_header()
        header.click_action_button('allusersbutton')

        # check label again
        self.assertThat(
            label,
            Eventually(Equals("<b>Best scores for all players</b>")))

    def test_enter_and_cancel(self):
        # find the first button that has a blank value
        gridButtons = self.main_view.get_blank_inputs()
        gridButton = gridButtons[0]

        # create a value function to check later using id
        buttonValue = lambda: self.main_view.select_single(
            "QQuickText", id=gridButton.id).text

        # double check that it's blank
        self.assertThat(buttonValue, Eventually(Equals("")))

        # click the button
        self.pointing_device.click_object(gridButton)

        # make that we can see the input screen
        self.main_view.get_number_dialog()

        # set a value, choose 4
        dialogButton = self.main_view.get_dialog_button("4")
        self.pointing_device.click_object(dialogButton)

        # check the value to ensure it worked
        self.assertThat(buttonValue, Eventually(Equals("4")))

        # click the button
        self.pointing_device.click_object(gridButton)

        # make sure that we can see the input screen
        self.main_view.get_number_dialog()

        # set a value, choose clear
        dialogButton = self.main_view.get_dialog_button("Cancel")
        self.pointing_device.click_object(dialogButton)

        # check the value to ensure it worked
        self.assertThat(buttonValue, Eventually(Equals("4")))

    def test_new_game_button(self):
        # testing new game with moderate mode
        self._set_difficulty(2, "Moderate")
        self._verify_game_start()

        # testing new game with always ask
        self._set_difficulty(6, "Always ask")

        # testing new game with always ask mode - easy
        self._verify_game_start(True, "easyGameButton")

        # testing new game with always ask mode - moderate
        self._verify_game_start(True, "moderateGameButton")

        # testing new game with always ask mode - hard
        self._verify_game_start(True, "hardGameButton")

        # testing new game with always ask mode - ultra hard
        self._verify_game_start(True, "ultrahardGameButton")

    def test_about_tab(self):
        # Switch to the 'About' tab
        self.main_view.switch_to_tab("aboutTab")

        # Check image loads
        aboutImage = lambda: self.main_view.select_single(
            "QQuickImage", objectName="aboutImage").progress
        self.assertThat(aboutImage, Eventually(Equals(1.0)))

        # Check the 'Author(s):' label is displayed
        aboutLabel = lambda: self.main_view.select_single(
            "Label", objectName="authorLabel").text
        self.assertThat(aboutLabel, Eventually(Equals("Author(s): ")))

        # Check the 'Contact:' label is displayed
        contactLabel = lambda: self.main_view.select_single(
            "Label", objectName="contactLabel").text
        self.assertThat(contactLabel, Eventually(Equals("Contact: ")))

        # Check correct Launchpad URL: is displayed
        urlLabel = lambda: self.main_view.select_single(
            "Label", objectName="urlLabel").text
        self.assertThat(urlLabel, Eventually(Equals(
            '<a href="https://launchpad.net/sudoku-app">'
            'https://launchpad.net/sudoku-app</a>')))

        # Check the 'Version:' label is displayed
        versionLabel = lambda: self.main_view.select_single(
            "Label", objectName="versionLabel").text
        self.assertThat(versionLabel, Eventually(Equals("Version: ")))

        # Check correct version is displayed
        version = lambda: self.main_view.select_single("Label",
                                                       objectName="version").text
        self.assertThat(version, Eventually(Equals("1.5")))

        # Check correct year is displayed
        yearLabel = lambda: self.main_view.select_single(
            "Label", objectName="yearLabel").text
        self.assertThat(yearLabel, Eventually(Equals("2013")))

    def test_hint_button(self):
        # open settings tab
        self.main_view.switch_to_tab("settingsTab")

        # click on hints switch to enable hints toolbar button
        hintsSwitchClickable = self.main_view.get_hints_switchClickable()

        self.pointing_device.click_object(hintsSwitchClickable)

        # verify hints switch is clicked
        self.assertThat(self.main_view.get_hints_switch().checked,
                        Eventually(Equals(True)))

        # exit settings tab by clicking on sudoku tab
        self.main_view.switch_to_tab("MainTab")

        # click on hint button on toolbar
        header = self.main_view.get_header()
        header.click_action_button('hintbutton')

        number_of_hints = lambda: self.main_view.select_single(
            objectName="blockgrid").numberOfHints
        self.assertThat(number_of_hints, Eventually(Equals(1)))

    def test_theme_change(self):
        # open settings tab
        self.main_view.switch_to_tab("settingsTab")

        #******** check theme selector  ********
        themeSelector = self.main_view.get_theme_selector()

        # select UbuntuColours option
        themeSelector.select_option('Label', text='UbuntuColours')
        self.assertThat(
            themeSelector.get_current_label().text,
            Eventually(
                Equals("UbuntuColours")))

        # select Simple theme option
        themeSelector.select_option('Label', text='Simple')
        self.assertThat(
            themeSelector.get_current_label().text,
            Eventually(
                Equals("Simple")))

        # select UbuntuColours theme option again
        themeSelector.select_option('Label', text='UbuntuColours')
        self.assertThat(
            themeSelector.get_current_label().text,
            Eventually(
                Equals("UbuntuColours")))

    def test_difficulty_selector(self):
        # open settings tab
        self.main_view.switch_to_tab("settingsTab")

        #******** check difficulty selector  ********
        difficulty = self.main_view.get_difficulty_selector()

        # select Easy
        difficulty.select_option('Label', text='Easy')
        self.assertThat(
            difficulty.get_current_label().text,
            Eventually(
                Equals("Easy")))

        # select Moderate
        difficulty.select_option('Label', text='Moderate')
        self.assertThat(
            difficulty.get_current_label().text,
            Eventually(
                Equals("Moderate")))

        # select Hard
        difficulty.select_option('Label', text='Hard')
        self.assertThat(
            difficulty.get_current_label().text,
            Eventually(
                Equals("Hard")))

        # select Ultra Hard
        difficulty.select_option('Label', text='Ultra Hard')
        self.assertThat(
            difficulty.get_current_label().text,
            Eventually(
                Equals("Ultra Hard")))

        # select Always ask
        difficulty.select_option('Label', text='Always ask')
        self.assertThat(
            difficulty.get_current_label().text,
            Eventually(
                Equals("Always ask")))

    def test_hint_switch(self):
        # open settings tab
        self.main_view.switch_to_tab("settingsTab")

        #******** check hint switch  ********
        # select hints switch
        hintsSwitchClickable = self.main_view.get_hints_switchClickable()
        self.assertThat(hintsSwitchClickable.text, Eventually(Equals("Hints")))
        hintsSwitch = self.main_view.get_hints_switch()

        # switch it on or off depending on it's state
        self.pointing_device.click_object(hintsSwitchClickable)
        self.assertThat(hintsSwitch.checked, Eventually(Equals(True)))

    def test_profiles(self):
        # open settings tab
        self.main_view.switch_to_tab("settingsTab")

        #******** check profile settings ********
        # select current profile
        currentProfile = self.main_view.get_current_profile()
        self.pointing_device.click_object(currentProfile)

        # let's change profile
        # select "sudoku user" profile
        sudokuUserProfile = self.main_view.get_sudoku_user_profile()
        self.pointing_device.click_object(sudokuUserProfile)

        # verify changed profile
        currentProfile = self.main_view.get_current_profile()
        self.assertThat(currentProfile.value, Equals("Sudoku User"))

        # let's add a user profile
        # verify add profile page opens
        sudokuAddProfile = self.main_view.get_add_profile()
        self.pointing_device.click_object(sudokuAddProfile)

        sudokuAddProfileDialog = self.main_view.get_add_profile_dialog()

        # insert Lastname
        lastName = self.main_view.get_add_profile_Lastname_field()
        self.pointing_device.click_object(lastName)
        self.assertThat(lastName.placeholderText,
                        Eventually(Equals("Lastname")))
        self.keyboard.type("Mylastname")
        self.assertThat(lastName.text, Eventually(Equals("Mylastname")))

        # insert Firstname
        firstName = self.main_view.get_add_profile_Firstname_field()
        self.pointing_device.click_object(firstName)
        self.assertThat(firstName.placeholderText,
                        Eventually(Equals("Firstname")))
        self.keyboard.type("Myfirstname")
        self.assertThat(firstName.text, Eventually(Equals("Myfirstname")))

        # click OK button
        OKButton = self.main_view.get_add_profile_OKbutton()
        self.assertThat(OKButton.buttonText, Eventually(Equals("OK")))
        self.pointing_device.click_object(OKButton)
        sudokuAddProfileDialog.wait_until_destroyed()

        #******** check manage profiles ********
        # select manage profile
        x, y, _, _ = self.main_view.globalRect
        line_x = x + self.main_view.width * 0.50
        start_y = y + self.main_view.height * 0.75
        stop_y = y + self.main_view.height * 0.6

        self.pointing_device.drag(line_x, start_y, line_x, stop_y)
        self._wait_to_stop_moving()

        manageProfile = self.main_view.get_manage_profiles()
        self.pointing_device.click_object(manageProfile)

        # click on the new profile just added
        myProfile = self.main_view.wait_select_single(
            "Standard",
            text="Myfirstname Mylastname")
        self.assertThat(myProfile.text,
                        Eventually(Equals("Myfirstname Mylastname")))
        self.pointing_device.click_object(myProfile)

        # click on delete
        deleteButton = self.main_view.get_edit_profile_delete_button()
        self.assertThat(deleteButton.buttonText, Eventually(Equals("Delete")))
        self.pointing_device.click_object(deleteButton)

        # check and make sure the profile is gone

    def _wait_to_stop_moving(self):
        self.main_view.select_single(
            'QQuickFlickable',
            objectName='settingsContainer').moving.wait_for(False)

    def _set_difficulty(self, selection, label):
        # open settings tab
        self.main_view.switch_to_tab("settingsTab")

        # set the difficulty of the game
        difficulty = self.main_view.get_difficulty_selector()

        # select Easy
        difficulty.select_option('Label', text=label)
        self.assertThat(
            difficulty.get_current_label().text,
            Eventually(
                Equals(label)))

    def _verify_game_start(self, askmode=False, button=None):
        # check the game starts properly (according to difficulty)
        self.main_view.switch_to_tab("MainTab")
        header = self.main_view.get_header()
        header.click_action_button('newgamebutton')

        # if we're in ask mode, make sure we can grab all the buttons
        # and click the proper button
        if askmode:
            self.assertThat(
                self.main_view.get_new_game_easy_button().buttonText,
                Eventually(Equals("Easy")))
            self.assertThat(
                self.main_view.get_new_game_moderate_button().buttonText,
                Eventually(Equals("Moderate")))
            self.assertThat(
                self.main_view.get_new_game_hard_button().buttonText,
                Eventually(Equals("Hard")))
            self.assertThat(
                self.main_view.get_new_game_ultrahard_button().buttonText,
                Eventually(Equals("Ultra\nHard")))
            self.pointing_device.click_object(
                self.main_view.get_new_game_button(button))

        number_of_hints = lambda: self.main_view.select_single(
            objectName="blockgrid").numberOfHints
        number_of_actions = lambda: self.main_view.select_single(
            objectName="blockgrid").numberOfActions

        self.assertThat(number_of_hints, Eventually(Equals(0)))
        self.assertThat(number_of_actions, Eventually(Equals(0)))

        # verify clock is moving
        game_seconds = self.main_view.select_single(
            objectName="blockgrid").gameSeconds
        self.assertThat(
            self.main_view.select_single(objectName="blockgrid").gameSeconds,
            Eventually(NotEquals(game_seconds)))
