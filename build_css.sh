#!/usr/bin/env bash

lessc -x csf/static/less/bootstrap.less>csf/static/css/bootstrap.css
lessc -x csf/static/less/responsive.less>csf/static/css/responsive.css
lessc -x csf/static/less/main.less>csf/static/css/main.css
