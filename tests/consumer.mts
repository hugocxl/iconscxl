import { createElement, createRef, type ComponentRef } from 'react';
import { SearchIcon } from '@hugocxl/iconscxl/react';
import { TerminalIcon } from '@hugocxl/iconscxl/react/terminal';

createElement(SearchIcon, { size: 24, ref: createRef<SVGSVGElement>(), 'aria-label': 'Search' });
createElement(TerminalIcon, { color: 'red', onClick: event => event.currentTarget.focus() });
// @ts-expect-error size must be numeric
createElement(SearchIcon, { size: 'large' });

import { SearchIcon as searchSvg } from '@hugocxl/iconscxl/js';
import { SearchIcon as rootSvg } from '@hugocxl/iconscxl';
const svg: string = searchSvg;
const same: string = rootSvg;

import { SearchIcon as SolidSearchIcon } from '@hugocxl/iconscxl/react/solid';
import { SearchIcon as StrokeSearchIcon } from '@hugocxl/iconscxl/react/stroke/search';
import { SearchIcon as DuotoneSearchIcon } from '@hugocxl/iconscxl/react/duotone/search';
import { SearchIcon as solidSvg } from '@hugocxl/iconscxl/js/solid';
createElement(SolidSearchIcon, { ref: createRef<SVGSVGElement>(), 'aria-label': 'Search' });
createElement(StrokeSearchIcon, { size: 16 });
createElement(DuotoneSearchIcon, { size: 32 });
const styledSvg: string = solidSvg;
// @ts-expect-error retained brands are not exported as invented stroke variants
import { GithubIcon } from '@hugocxl/iconscxl/react/stroke';
