# -*- coding: utf-8 -*-
using CairoMakie: Cycle, Theme

colors = [:black, :red, :blue, :green, :purple]
marker = [:rect, :dtriangle, :diamond, :xcross, :star4]

paper_theme = Theme(
    backgroundcolor = :white,
    resolution      = (1600, 1200),
    fontsize        = 48,

    palette = (
        color       = colors,
        strokecolor = colors,
        marker      = marker
    ),

    Axis = (
        xgridstyle  = :dash,
        ygridstyle  = :dash
    ),
    
    Lines = (
        linewidth   = 2.5,
        linestyle   = :dash
    ),
    
    Scatter = (
        markersize  = 30,
        strokewidth = 1.5,
        color       = :transparent,
        cycle       = Cycle([:strokecolor, :marker], covary = true)
    )
)
