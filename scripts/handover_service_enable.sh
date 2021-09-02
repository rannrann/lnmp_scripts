#!/bin/bash
systemctl stop nginx php-fpm
systemctl enable nginx php-fpm mariadb --now