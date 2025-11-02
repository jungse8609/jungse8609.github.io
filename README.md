# 자동화 스크립트

- hide.py: 2달 이상 지난 포스트들은 감춘다.
    - settings.json 업데이트
    - `_posts/`, `assets/img/_posts/` 경로 파일들 감춤
- trim.py: 노션에서 복사/붙여넣기한 텍스트의 이미지 경로를 수정한다.
    - 노션에서 복사한 이미지 경로 텍스트는 [!image](KEY Value) 이다.
    - ![image.png](../assets/img/posts/20xx-xx-xx-title/image (index).png)로 수정한다.
- new.py: 새로운 포스트를 작성한다.
    - Input 1. 파일명: (오늘 일자)-(파일명).md로 생성한다.
    - Input 2. 제목: 포스트 제목
    - Input 3. 카테고리: 카테고리를 작성하고 태그에 자동으로 카테고리를 소문자로 넣는다.

# Chirpy Starter

[![Gem Version](https://img.shields.io/gem/v/jekyll-theme-chirpy)][gem]&nbsp;
[![GitHub license](https://img.shields.io/github/license/cotes2020/chirpy-starter.svg?color=blue)][mit]

When installing the [**Chirpy**][chirpy] theme through [RubyGems.org][gem], Jekyll can only read files in the folders
`_data`, `_layouts`, `_includes`, `_sass` and `assets`, as well as a small part of options of the `_config.yml` file
from the theme's gem. If you have ever installed this theme gem, you can use the command
`bundle info --path jekyll-theme-chirpy` to locate these files.

The Jekyll team claims that this is to leave the ball in the user’s court, but this also results in users not being
able to enjoy the out-of-the-box experience when using feature-rich themes.

To fully use all the features of **Chirpy**, you need to copy the other critical files from the theme's gem to your
Jekyll site. The following is a list of targets:

```shell
.
├── _config.yml
├── _plugins
├── _tabs
└── index.html
```

To save you time, and also in case you lose some files while copying, we extract those files/configurations of the
latest version of the **Chirpy** theme and the [CD][CD] workflow to here, so that you can start writing in minutes.

## Usage

Check out the [theme's docs](https://github.com/cotes2020/jekyll-theme-chirpy/wiki).

## Contributing

This repository is automatically updated with new releases from the theme repository. If you encounter any issues or want to contribute to its improvement, please visit the [theme repository][chirpy] to provide feedback.

## License

This work is published under [MIT][mit] License.

[gem]: https://rubygems.org/gems/jekyll-theme-chirpy
[chirpy]: https://github.com/cotes2020/jekyll-theme-chirpy/
[CD]: https://en.wikipedia.org/wiki/Continuous_deployment
[mit]: https://github.com/cotes2020/chirpy-starter/blob/master/LICENSE
