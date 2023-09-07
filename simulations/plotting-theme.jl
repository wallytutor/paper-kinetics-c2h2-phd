# -*- coding: utf-8 -*-
using CairoMakie: Cycle, Theme

colors = [:black, :red, :blue, :green, :purple, :magenta]
marker = [:rect, :dtriangle, :diamond, :xcross, :star4, :utriangle]

paper_theme = Theme(
    backgroundcolor  = :white,
    resolution       = (1600, 1200),
    fontsize         = 48,
    figure_padding   = (30, 80, 30, 30),

    palette = (
        color        = colors,
        strokecolor  = colors,
        marker       = marker
    ),

    Axis = (
        xgridstyle   = :dash,
        ygridstyle   = :dash,
        xgridwidth   = 3.0,
        ygridwidth   = 3.0
    ),

    Lines = (
        linewidth    = 2.5,
        linestyle    = :dash
    ),

    Scatter = (
        markersize   = 30,
        strokewidth  = 1.5,
        color        = :transparent,
        cycle        = Cycle([:strokecolor, :marker], covary = true)
    ),

    Legend = (
        framevisible = false,
        labelsize    = 36,
    ),
)
