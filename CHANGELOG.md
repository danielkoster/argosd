# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [1.4.0] - 2018-12-18
### Changed
- Download torrents through requests library instead of Transmission itself

## [1.3.0] - 2018-11-27
### Changed
- Added "on delete cascade" to foreign key

### Removed
- Removed default echo handler from Telegram bot

## [1.2.1] - 2017-10-16
### Fixed
- Added missing import statement

## [1.2.0] - 2017-10-13
### Added
- #38 Add interactive Telegram commands
  This adds a "Download now" button to messages about new matching episodes from the RSS feed.
- #43 Alter directory structure to suit Plex
  The strategy used to create directory names can now be changed to a Plex supported format.
- Added this changelog

### Changed
- #41 Code improvements
  - Simplified code, minor restructuring
  - Removed download functionality from model
- #44 Let systemd service wait for network-online

## [1.1.0] - 2016-10-30
### Added
- #29 Store shows in subdirectories
- #30 Send a notification on download
  This adds a Telegram bot which can be used to recieve notifications about downloaded episodes.

### Fixed
- #32 Spawn API process without inheriting resources

## [1.0.2] - 2016-09-17
### Removed
- "link" attribute is no longer shown in the /episodes API endpoint
- Removed unused "tmdb_id" attribute from episodes

### Fixed
- #24 API call to episodes raises exception

## [1.0.1] - 2016-09-17
### Fixed
- #20 Existing torrent in client should not be added again
- #19 Downloaded episode is saved again

## [1.0.0] - 2016-09-15
### Added
- The first production-ready release.

## 0.1.0 - 2016-09-06
### Added
- This is the initial version. It is still in development and has not been used in a production environment.

[1.4.0]: https://github.com/danielkoster/argosd/compare/v1.3.0...v1.4.0
[1.3.0]: https://github.com/danielkoster/argosd/compare/v1.2.1...v1.3.0
[1.2.1]: https://github.com/danielkoster/argosd/compare/v1.2.0...v1.2.1
[1.2.0]: https://github.com/danielkoster/argosd/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/danielkoster/argosd/compare/v1.0.2...v1.1.0
[1.0.2]: https://github.com/danielkoster/argosd/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/danielkoster/argosd/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/danielkoster/argosd/compare/v0.1.0...v1.0.0
