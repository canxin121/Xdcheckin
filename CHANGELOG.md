# Changelog

Changelog for Xdcheckin.

## [Unreleased]

## [3.6.5] - 2024-09-26

# Added

- Add support for IPv6.

## [3.6.4] - 2024-09-26

# Fixed

- (APP) Fix another startup crash.

## [3.6.3] - 2024-09-26

# Fixed

- (APP) Fix startup crash.

## [3.6.2] - 2024-09-26

# Fixed

- (Webpage) Possible fix for "zbarWasm is not defined" error.

## [3.6.1] - 2024-09-25

# Added

- (Server/Webpage) Add support for qrcode scanning on iOS devices. Needs ``xdcheckin[image]`` to be installed on the server.
- (Module) Add ``xdcheckin.video_get_img()``, ``xdcheckin.img_scan()``, ``xdcheckin.classroom_urls`` and ``xdcheckin.classroom_url_get_single()``. Refer to source code for details.
- Add two locations for the north campus. (@wtflmao )

## [3.5.8] - 2024-09-25

# Fixed

- Fix "Please use Xuezaixidian APP to sign in" failure.

## [3.5.7] - 2024-09-24

# Added

- (Webpage) Nuke AliPlayer telemetrics.

## [3.5.6] - 2024-09-23

# Added

- (Webpage) Add support for Safari 10.1.

## [3.5.5] - 2024-09-20

# Added

- Redo display error message for qrcode scanning.

## [3.5.4] - 2024-09-19

# Added

- Display error message for qrcode scanning.
- (Module) Add ```xdcheckin.Chaoxing.login_username_xxt``` and ```xdcheckin.Chaoxing.login_username_2```.
- Mock IP address.

## [3.5.3] - 2024-09-14

# Fixed

- Checkin failure caused by device identifier.

## [3.5.2] - 2024-09-14

# Changed

- Activities will now be fetched much faster with a new API.

## [3.5.1] - 2024-09-13

### Added

- (Module) Added ```xdcheckin.Chaoxing.checkin_get_info_widget()``` API.

### Changed

- (Module) Rename ```xdcheckin.Chaoxing.checkin_get_details()``` to ```xdcheckin.Chaoxing.checkin_get_info_newsign()```, ```xdcheckin.Chaoxing.checkin_get_pptactiveinfo()``` to ```xdcheckin.Chaoxing.checkin_get_info_ppt()```.

## [3.4.6] - 2024-09-12

### Removed

- (Module) Remove unused debug messages.

## [3.4.5] - 2024-09-12

### Added

- Added mechanisms against anti-mock-location detection.
- (Module) Add ```xdcheckin.Chaoxing.name``` property for student name.

## [3.4.4] - 2024-09-12

### Fixed

- (Module) Fix curriculum timetable being truncated.
- (Webpage) Fix curriculum table not shown.

## [3.4.3] - 2024-09-02

### Fixed

- Fix EULA dialog ineffective.

## [3.4.2] - 2024-09-01

### Fixed

- Fix login failure.

## [3.4.1] - 2024-09-01

### Fixed

- Fix false success for IDS login.

### Removed

- Remove broken ```xdcheckin.IDSSession.login_cookies()```.

## [3.3.3] - 2024-08-26

### Changed

- Update dependencies.

## [3.3.2] - 2024-08-06

### Changed

- Optimize courses fetching.
- Update a classifier in project metadata.

## [3.3.1] - 2024-07-04

### Added

- (Webpage) TeacherFull is now scannable.

## [3.2.1] - 2024-07-04

### Added

- (Module) Add new login method ``xdcheckin.Chaoxing.login_username_yz()``.

### Changed

- Use ``zbar-wasm`` to handle qrcode decoding for better performance and data usage.
- (Module) Remove unused dependencies.

## [3.1.1] - 2024-06-24

### Added

- (Module) Rework IDSSession to support logging in with phone number and dynamic code. See the code for details.

### Fixed

- (Module) Fix ``xdcheckin.IDSSession.login_cookies()`` failures.
- (APP) Fix adaptive icon on Android.

### Changed

- (Module) Optimize performance and precision of ``xdcheckin.solve_captcha()``.

## [3.0.2] - 2024-06-10

### Fixed

- (Server) Fix incomplete server shutdown.
- Fix some login errors.
- (APP) Fix missing APP icon on Android.
- (Module) Fix compability with Python 3.9.

### Removed

- (Module) Remove obsolete ``xdcheckin.Chaoxing.login_username_xxk()``.

## [3.0.1] - 2024-06-10

### Added

- (Module) Add shortcuts ``xdcheckin.Chaoxing``, ``xdcheckin.IDSSession``, ``xdcheckin.Newesxidian``, ``xdcheckin.locations``, ``xdcheckin.server_routes``, ``xdcheckin.create_server``, ``xdcheckin.start_server`` and ``xdcheckin.solve_captcha`` for easier importing.
- (Module) ``xdcheckin.Chaoxing`` now provides ``uid`` and ``fid`` attributes for access.

### Fixed

- Fix classroom livestream not available on webpage for some XDU(-related) students.
- (Module) Fix wrong and missing comment headers.
- (Module) Resource and session cleanup on APP exit is now properly handled.
- Other minor fixes.

### Removed

- (Module) Remove obsolete ``xdcheckin.Chaoxing().login_username_v5()`` and ``xdcheckin.Chaoxing().login_username_v11()`` login methods.
- (Module) Remove unused dependencies.

### Changed

- Optimize speed for activities fetching and checking in.
- Optimize messages for check-in failure for better reading and parsing.
- (APP/Module/Server) ``xdcheckin.Chaoxing``, ``xdcheckin.IDSSession``, ``xdcheckin.Newesxidian`` and vast majority of ``xdcheckin`` are now made async with ``asyncio`` and ``aiohttp`` for security and performance. Refer to source code for details.
- (Module) Some attributes and methods of the classes are now made private for security.
- (Module) Rename the ``logined`` attribute to ``logged_in`` of ``xdcheckin.Chaoxing``, ``xdcheckin.IDSSession`` and ``xdcheckin.Newesxidian``.
- (Module) Replace some dependencies.
- (Server) Change commandline messages.
- Optimize secrets generation for Chaoxing CAPTCHAs.
- Optimize webpage loading speed.

## [2.1.1] - 2024-05-14

### Fixed

- Fix some courses missing and not queried for activities.

### Removed

- (Module) Remove ```xdcheckin.core.chaoxing.Chaoxing().checkin_get_location_log()```.

## [2.0.12] - 2024-04-29

### Fixed

- Update API for course fetching to bypass Chaoxing's IP blacklist.

## [2.0.11] - 2024-04-28

### Fixed

- Course fetching will fallback to use curriculum lessons in case IP is blacklisted by Chaoxing.

### Changed

- Improve server session vacuum worker.

## [2.0.10] - 2024-04-27

### Added

- Server will now automatically vacuum old sessions.

## [2.0.9] - 2024-04-27

### Fixed

- Fix failure fetching signle activity when end time is missing.

## [2.0.8] - 2024-04-21

### Fixed

- Fix CAPTCHA triggered on other failures for location checkin.

### Changed

- (Module) Improve accuracy and performance of ```xdcheckin.util.chaoxing_captcha.solve_captcha()```.

## [2.0.7] - 2024-04-15

### Changed

- (Module) Improve accuracy and performance of ```xdcheckin.util.chaoxing_captcha.solve_captcha()```.

## [2.0.6] - 2024-04-14

### Changed

- (Module) Improve accuracy of ```xdcheckin.util.chaoxing_captcha.solve_captcha()```.

## [2.0.5] - 2024-04-14

### Added

- (Module) Lightweight ```xdcheckin.util.chaoxing_captcha.solve_captcha()``` for solving slider CAPTCHA in a non-GUI environment. Returns slider offset.

## [2.0.4] - 2024-04-09

### Fixed

- Fix classroom name not displayed properly if chosen via curriculum.

## [2.0.3] - 2024-04-09

### Fixed

- Fix curriculum not peoperly displayed in existence of courses without classroom.

## [2.0.2] - 2024-04-06

### Added

- (Module) ```xdcheckin.core.xidian.Newesxidian().curriculum_get_curriculum()``` can specify week number, and livestream now contains classroom location.

### Fixed

- Fix error when already checked-in.

## [2.0.1] - 2024-04-05

### Added

- Support check-ins with CAPTCHA verification.

### Changed

- (Module) ```xdcheckin.core.chaoxing.Chaoxing().checkin_do_presign()``` now returns presign state, location and CAPTCHA ID on success.
- (Module) Add ```xdcheckin.core.chaoxing.Chaoxing().checkin_get_captcha()``` and ```xdcheckin.core.chaoxing.Chaoxing().checkin_verify_captcha()``` to support CAPTCHA verification.
- (Module) Make ```xdcheckin.core.chaoxing.Chaoxing().checkin_do_sign()``` standalone to support CAPTCHA verification.
- (Module) ```xdcheckin.core.chaoxing.Chaoxing().checkin_checkin_location()```, ```xdcheckin.core.chaoxing.Chaoxing().checkin_checkin_qrcode()``` and ```xdcheckin.core.chaoxing.Chaoxing().checkin_checkin_qrcode_url()``` now also return payload for ```xdcheckin.core.chaoxing.Chaoxing().checkin_do_sign()``` to support CAPTCHA verification. Their return values has been reformed accordingly.
- (Module) ```xdcheckin.core.chaoxing.Chaoxing().curriculum_get_curriculum()```, ```xdcheckin.core.xidian.Newesxidian().curriculum_get_curriculum()``` has their keys renamed to the proper plural forms. Classroom locations and livestreams are now stored in lists to support multiple values.

### Fixed

- Fix course with multiple classroom locations not properly shown in curriculum.

## [1.5.3] - 2024-03-28

### Added

- (Module) ```xdcheckin.core.chaoxing.Chaoxing().courses_get_courses()``` now contains course status, start and end time.

### Fixed

- Fix activity not properly shown.

### Changed

- Activities fetching will now filter ended courses.
- (Module) ```xdcheckin.core.chaoxing.Chaoxing().checkin_get_details()``` and ```xdcheckin.core.chaoxing.Chaoxing().checkin_get_pptactiveinfo()``` won't stringify values anymore.

## [1.5.2] - 2024-03-27

### Fixed

- Fix location address override not working.

## [1.5.1] - 2024-03-26

### Added

- Checkin's activity ID, start time and end time will now be displayed.
- (Module) New config ```chaoxing_course_get_activities_workers``` for workers count for xdcheckin.core.chaoxing.Chaoxing().course_get_activities()
- (Module) Add ```xdcheckin.core.chaoxing.Chaoxing().checkin_get_location_log()``` which returns a list of checkin locations submitted by others.

### Fixed

- Further some activities not fetched due to Chaoxing's anti spamming

### Changed

- (Module) Remove config ```chaoxing_checkin_location_address_override``` with its functionality taken by ```chaoxing_checkin_location_address_override_maxlen```.
- (Module) ```xdcheckin.core.chaoxing.Chaoxing().checkin_get_location()``` will not call ```xdcheckin.core.chaoxing.Chaoxing().checkin_format_location()``` automatically now.

## [1.4.1] - 2024-03-23

### Added

- (Module) Introduce the new activities fetching API as the default: xdcheckin.core.chaoxing.Chaoxing().course_get_course_activities_ppt().

### Fixed

- Fix some activities not fetched due to Chaoxing's anti spamming.

### Changed

- (Module) xdcheckin.core.chaoxing.Chaoxing().course_get_course_activities() has been renamed to xdcheckin.core.chaoxing.Chaoxing().course_get_course_activities_v2() and currently unused.

## [1.3.10] - 2024-03-23

### Fixed

- Fix several possible login errors.
- Fix checkin error if corresponding course is not in the course list.

## [1.3.9] - 2024-03-22

### Fixed

- Fix activities fetching error caused by empty end time

## [1.3.8] - 2024-03-22

# Added

- (Module) Activities now contain their start and end time.

# Fixed

- Optimize activities fetching logic in prevention of triggering Chaoxing's anti spamming mechanism.

## [1.3.7] - 2024-03-18

### Added

- (Module) Add xdcheckin.core.chaoxing.Chaoxing().checkin_format_location() to format checkin location based on config. Called automatically in xdcheckin.core.chaoxing.Chaoxing().checkin_get_location().

### Fixed

- Fix webpage title not properly displayed for non-XDUers.

### Changed

- Revert location fetching logic for location checkin due to Chaoxing API restabilization. This should provide more accuracy for location checkin.
- (Module) xdcheckin.core.chaoxing.Chaoxing().checkin_do_presign() now returns checkin location on success. You should call xdcheckin.core.chaoxing.Chaoxing().checkin_format_location() manually then.

## [1.3.6] - 2024-03-15

### Fixed

- Fix hidden camera on normal devices.

### Changed

- Checkin location address override now only affects addresses shorter than 13.

## [1.3.5] - 2024-03-15

### Added

- Automatically hide camera if device is unavailable.
- Properly formatted changelog.

## [1.3.4] - 2024-03-14

### Added

- Introduce randomness to checkin location coordinates for anti-detection.
- User-given location address is now passed through for checking-in for anti-detection.

## [1.3.3] - 2024-03-13

### Fixed

- (Android) version 1.3.2 crashes on start.
- (Module) ```xdcheckin.app``` is now properly unimportable.

### Changed

- (Android) APP signature is changed. Please uninstall before upgrading from earlier versions.

## [1.3.2] - 2024-03-10

### Fixed

- Fix false alert on logout failure.

### Changed

- IDS captcha has been changed to a floating image instead of a red line.
- Change text of activity buttons.

## [1.3.1] - 2024-03-09

### Added

- IDS login support.
- Automatic login support.

### Changed

- Optimize curriculum loading speed.

### Fixed

- PPTVideo image is now uncompressed in case of qrcode not detected errors.
- Various other fixes.

## [1.2.11] - 2024-03-04

### Fixed

- Fix multiuser dysfunctionality and security issues related to session data.

### Changed

- Optimize curriculum text and layout.
- (Module) Newesxidian has been splitted to xdcheckin.core.xidian.Newesxidian.

## [1.2.10] - 2024-03-02

### Added

- Classroom "Load" and "Extract" buttons are now moved to classroom list.

### Fixed

- (Module) Fix missing data files.

## [1.2.9] - 2024-03-02

### Added

- Video players are now automatically resized.

### Changed

- Further simplify button text.
- Webpage is now displayed bigger for easier usage.

### Removed

- Remove the "Resize All" button.

## [1.2.8] - 2024-03-01

### Added

- Other video players will now be muted automatically when unmuting one.
- Confirmation dialog before logging out.
- (Module) Xdcheckin is now an importable module with ```xdcheckin-server``` cli tool.

## [1.2.7] - 2024-02-28

### Added

- Added functionalities for logging out and logging in again.

### Fixed

- Fix login failure after preceding failure.
- Fix curriculum loading failure after preceding failure.
- APP version will now properly show up in the page footer.
- Login error messages are now properly generated.
- Fix video players, locations and classrooms list failures.

### Changed

- Move "Input Location" and "I'm Feeling Lucky" under their corresponding list.

### Removed

- Remove the "Unmute All" and "Mute All" buttons.

## [1.2.6] - 2024-02-26

### Added

- Page footer will now display APP version.

### Fixed

- Fix zero-sized video players.
- Fix a bug causing login failure.
- Login error message will now be properly displayed.
- (Windows/macOS) Fix APP crash failure.

## [1.2.5] - 2024-02-26

### Changed

- Optimized login and curriculum loading logic.

## [1.2.4] - 2024-02-25

### Fixed

- Fix location checkin failure.

## [1.2.3] - 2024-02-25

### Added

- Curriculum info will now be displayed.

### Fixed

- Current location info will now be properly displayed.

### Changed

- Optimized data usage and responsiveness of qrcode checkin.

## [1.2.2] - 2024-02-24

### Added

- Livestream URLs with blank or missing perspectives are now supported.

### Changed

- Fully updated livestream URLs list.

### Fixed

- Fix classroom switching failure.

## [1.2.1] - 2024-02-22

### Added

- Lesson time is now displayed in curriculum.


### Fixed

- Wrong curriculum year due to Chaoxing's broken API.

## [1.2.0] - 2024-02-22

### Added

- Livestream info is now displayed in curriculum.

## [1.1.8] - 2024-02-09

### Fixed

- (Android) Text will now wrap properly.

## [1.1.7] - 2024-02-08

### Fixed

- APP will now properly stop the backend server on exit.

### Removed

- (Linux) Remove APP WebView to fix crashes with unmet dependencies. Thus this is the first usable version.
- (Android) Remove APP WebView since it's useless.

## [1.1.6] - 2024-01-19

### Added

- (Android) APP will now automatically open the webpage.

## [1.1.5] - 2024-01-17

### Added

- Checking-in is now multithreaded for speed.
- Several responses are now cached for reusage and speed.

### Changed

- Activities fetching will now be cached for 60 seconds. Please wait before fetching again.

## [1.1.4] - 2024-01-13

### Fixed

- Activities fetching is now multithreaded for speed.
- Fix non-ranged location or qrcode checkin failure due to further Chaoxing's API changes.

### Changed

- Optimized webpage loading speed.
- Activities fetching is now limited to 48 courses.

## [1.1.3] - 2024-01-09

### Added

- Display more details in checkin result and alert.

### Fixed

- Fix non-ranged location checkin failure due to Chaoxing's API changes.

## [1.1.2] - 2024-01-07

### Fixed

- Fix qrcode checkin failure due to Chaoxing's API changes.

## [1.1.1] - 2024-01-06

### Added

- Added camera section which is also available for qrcode scanning.

### Fixed

- (Android) Fix a bug causing newly installed APP to crash.

## [1.0.4] - 2024-01-06

### Changed

- Backend restructure.

## [1.0.3] - 2024-01-05

### Added

- Cooldown for location checkin buttons to avoid spamming.
- Replace cookies with local storage for security.

## [1.0.2] - 2024-01-04

### Added

- Cooldown for scan button to avoid spamming.

## [1.0.1] - 2024-01-01

### Fixed

- Fix scan button not properly hidden before logged in.

### Changed

- Pyzbar now replaces OpenCV for qrcode processing.
- (Windows) [Visual C++ Redistributable Packages for Visual Studio 2013](https://www.microsoft.com/en-US/download/details.aspx?id=40784) must be installed to use Pyzbar.

## [1.0.0] - 2024-01-01

### Changed

- OpenCV is now used for processing qrcode with accuracy and responsiveness.

## [0.0.18] - 2023-12-31

### Added

- Activities checking is now multithreaded for quicker responses.

[unreleased]: https://github.com/Pairman/Xdcheckin/compare/3.6.5...main
[3.6.5]: https://github.com/Pairman/Xdcheckin/compare/3.6.4...3.6.5
[3.6.4]: https://github.com/Pairman/Xdcheckin/compare/3.6.3...3.6.4
[3.6.3]: https://github.com/Pairman/Xdcheckin/compare/3.6.2...3.6.3
[3.6.2]: https://github.com/Pairman/Xdcheckin/compare/3.6.1...3.6.2
[3.6.1]: https://github.com/Pairman/Xdcheckin/compare/3.5.8...3.6.1
[3.5.8]: https://github.com/Pairman/Xdcheckin/compare/3.5.7...3.5.8
[3.5.7]: https://github.com/Pairman/Xdcheckin/compare/3.5.6...3.5.7
[3.5.6]: https://github.com/Pairman/Xdcheckin/compare/3.5.5...3.5.6
[3.5.5]: https://github.com/Pairman/Xdcheckin/compare/3.5.4...3.5.5
[3.5.4]: https://github.com/Pairman/Xdcheckin/compare/3.5.3...3.5.4
[3.5.3]: https://github.com/Pairman/Xdcheckin/compare/3.5.2...3.5.3
[3.5.2]: https://github.com/Pairman/Xdcheckin/compare/3.5.1...3.5.2
[3.5.1]: https://github.com/Pairman/Xdcheckin/compare/3.4.6...3.5.1
[3.4.6]: https://github.com/Pairman/Xdcheckin/compare/3.4.5...3.4.6
[3.4.5]: https://github.com/Pairman/Xdcheckin/compare/3.4.4...3.4.5
[3.4.4]: https://github.com/Pairman/Xdcheckin/compare/3.4.3...3.4.4
[3.4.3]: https://github.com/Pairman/Xdcheckin/compare/3.4.2...3.4.3
[3.4.2]: https://github.com/Pairman/Xdcheckin/compare/3.4.1...3.4.2
[3.4.1]: https://github.com/Pairman/Xdcheckin/compare/3.3.3...3.4.1
[3.3.3]: https://github.com/Pairman/Xdcheckin/compare/3.3.2...3.3.3
[3.3.2]: https://github.com/Pairman/Xdcheckin/compare/3.3.1...3.3.2
[3.3.1]: https://github.com/Pairman/Xdcheckin/compare/3.2.1...3.3.1
[3.2.1]: https://github.com/Pairman/Xdcheckin/compare/3.1.1...3.2.1
[3.1.1]: https://github.com/Pairman/Xdcheckin/compare/3.0.2...3.1.1
[3.0.2]: https://github.com/Pairman/Xdcheckin/compare/3.0.1...3.0.2
[3.0.1]: https://github.com/Pairman/Xdcheckin/compare/2.1.1...3.0.1
[2.1.1]: https://github.com/Pairman/Xdcheckin/compare/2.0.12...2.1.1
[2.0.12]: https://github.com/Pairman/Xdcheckin/compare/2.0.11...2.0.12
[2.0.11]: https://github.com/Pairman/Xdcheckin/compare/2.0.10...2.0.11
[2.0.10]: https://github.com/Pairman/Xdcheckin/compare/2.0.9...2.0.10
[2.0.9]: https://github.com/Pairman/Xdcheckin/compare/2.0.8...2.0.9
[2.0.8]: https://github.com/Pairman/Xdcheckin/compare/2.0.7...2.0.8
[2.0.7]: https://github.com/Pairman/Xdcheckin/compare/2.0.6...2.0.7
[2.0.6]: https://github.com/Pairman/Xdcheckin/compare/2.0.5...2.0.6
[2.0.5]: https://github.com/Pairman/Xdcheckin/compare/2.0.4...2.0.5
[2.0.4]: https://github.com/Pairman/Xdcheckin/compare/2.0.3...2.0.4
[2.0.3]: https://github.com/Pairman/Xdcheckin/compare/2.0.2...2.0.3
[2.0.2]: https://github.com/Pairman/Xdcheckin/compare/2.0.1...2.0.2
[2.0.1]: https://github.com/Pairman/Xdcheckin/compare/1.5.3...2.0.1
[1.5.3]: https://github.com/Pairman/Xdcheckin/compare/1.5.2...1.5.3
[1.5.2]: https://github.com/Pairman/Xdcheckin/compare/1.5.1...1.5.2
[1.5.1]: https://github.com/Pairman/Xdcheckin/compare/1.4.1...1.5.1
[1.4.1]: https://github.com/Pairman/Xdcheckin/compare/1.3.10...1.4.1
[1.3.10]: https://github.com/Pairman/Xdcheckin/compare/1.3.9...1.3.10
[1.3.9]: https://github.com/Pairman/Xdcheckin/compare/1.3.8...1.3.9
[1.3.8]: https://github.com/Pairman/Xdcheckin/compare/1.3.7...1.3.8
[1.3.7]: https://github.com/Pairman/Xdcheckin/compare/1.3.6...1.3.7
[1.3.6]: https://github.com/Pairman/Xdcheckin/compare/1.3.5...1.3.6
[1.3.5]: https://github.com/Pairman/Xdcheckin/compare/1.3.4...1.3.5
[1.3.4]: https://github.com/Pairman/Xdcheckin/compare/1.3.3...1.3.4
[1.3.3]: https://github.com/Pairman/Xdcheckin/compare/1.3.2...1.3.3
[1.3.2]: https://github.com/Pairman/Xdcheckin/compare/1.3.1...1.3.2
[1.3.1]: https://github.com/Pairman/Xdcheckin/compare/1.2.11...1.3.1
[1.2.11]: https://github.com/Pairman/Xdcheckin/compare/1.2.10...1.2.11
[1.2.10]: https://github.com/Pairman/Xdcheckin/compare/1.2.9...1.2.10
[1.2.9]: https://github.com/Pairman/Xdcheckin/compare/1.2.8...1.2.9
[1.2.8]: https://github.com/Pairman/Xdcheckin/compare/1.2.7...1.2.8
[1.2.7]: https://github.com/Pairman/Xdcheckin/compare/1.2.6...1.2.7
[1.2.6]: https://github.com/Pairman/Xdcheckin/compare/1.2.5...1.2.6
[1.2.5]: https://github.com/Pairman/Xdcheckin/compare/1.2.4...1.2.5
[1.2.4]: https://github.com/Pairman/Xdcheckin/compare/1.2.3...1.2.4
[1.2.3]: https://github.com/Pairman/Xdcheckin/compare/1.2.2...1.2.3
[1.2.2]: https://github.com/Pairman/Xdcheckin/compare/1.2.1...1.2.2
[1.2.1]: https://github.com/Pairman/Xdcheckin/compare/1.2.0...1.2.1
[1.2.0]: https://github.com/Pairman/Xdcheckin/compare/1.1.8...1.2.0
[1.1.8]: https://github.com/Pairman/Xdcheckin/compare/1.1.7...1.1.8
[1.1.7]: https://github.com/Pairman/Xdcheckin/compare/1.1.6...1.1.7
[1.1.6]: https://github.com/Pairman/Xdcheckin/compare/1.1.5...1.1.6
[1.1.5]: https://github.com/Pairman/Xdcheckin/compare/1.1.4...1.1.5
[1.1.4]: https://github.com/Pairman/Xdcheckin/compare/1.1.3...1.1.4
[1.1.3]: https://github.com/Pairman/Xdcheckin/compare/1.1.2...1.1.3
[1.1.2]: https://github.com/Pairman/Xdcheckin/compare/1.1.1...1.1.2
[1.1.1]: https://github.com/Pairman/Xdcheckin/compare/1.0.4...1.1.1
[1.0.4]: https://github.com/Pairman/Xdcheckin/compare/1.0.3...1.0.4
[1.0.3]: https://github.com/Pairman/Xdcheckin/compare/1.0.2...1.0.3
[1.0.2]: https://github.com/Pairman/Xdcheckin/compare/1.0.1...1.0.2
[1.0.1]: https://github.com/Pairman/Xdcheckin/compare/1.0.0...1.0.1
[1.0.0]: https://github.com/Pairman/Xdcheckin/compare/0.0.18...1.0.0
[0.0.18]: https://github.com/Pairman/Xdcheckin/tree/0.0.18
