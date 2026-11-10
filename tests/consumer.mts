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
