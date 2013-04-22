#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# fakeroute
#
# fakeroute intercept traceroute-like probes in order to simulate various
# topologies, including multipath due to per-flow load balancers.
#
# Authors: Jordan Augé       <jordan.auge@lip6.fr>
#          Marc-Olivier Buob <marc-olivier.buob@lip6.fr> 
#
# Copyright (C)2011-2013, UPMC Sorbonnes Universités / LIP6
#
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 3, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
# 
# You should have received a copy of the GNU General Public License along with
# this program; see the file COPYING.  If not, write to the Free Software
# Foundation, 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

import os, re, socket

#-----------------------------------------------------------------
# Constants
#-----------------------------------------------------------------

# Directory in which fakeroute expects some network topologies
CONFIGPATH = ["./targets", "~/.fakeroute/targets", "/etc/fakeroute/targets"]

#-----------------------------------------------------------------
# Messages
#-----------------------------------------------------------------

ERR_NO_CONF = "E: No configuration directory found in %r" % CONFIGPATH

#-----------------------------------------------------------------
# Load fakeroute file
#-----------------------------------------------------------------

def get_cfg_path():
    """
    \brief For each directory stored in CONFIGPATH, return the first
        existing directory. If no one exists, return None.
    \return The first valid configuration directory, None otherwise
    """
    for path in CONFIGPATH:
        if os.path.exists(path):
            return path
    return None

def sort_ip4_list(l):
    """
    \brief Sort a list of IPv4 address in the lexicographic order
    \param l The list to sort
    \return The corresponding sorted list
    """
    ll = [tuple(x.split('.')) for x in l]
    ll.sort()
    return ['.'.join(x) for x in ll]

def get_handled_files(cfg_path):
    """
    \brief Retrieve according to the filenames in 'cfg_path' the IPs
        handled by fakeroute.
    \param cfg_path The directory storing the network topology
        emulated by fakeroute.
    \return A pair made of two dictionnaries:
        handled4 { String: String } maps a target IPv4 with the filename it is issued
        handled6 { String: String } maps a target IPv6 with the filename it is issued
    """
    handled4, handled6 = ({}, {})
    filenames = os.listdir(cfg_path)
    for filename in filenames:
        m = re.match(r"(?P<ip>[0-9a-fA-F.\:]+)-.*", filename)
        if m:
            try:
                ip_version = str_ip_get_version(m.group("ip"))
                if ip_version == socket.AF_INET6:
                    handled6[filename.split('-')[0]] = os.path.join(cfg_path, filename)
                elif ip_version == socket.AF_INET: 
                    handled4[filename.split('-')[0]] = os.path.join(cfg_path, filename)
            except ValueError, why:
                print why
        else:
            print "I: Ignored target file '%s'" % filename
    return (handled4, handled6)

#-----------------------------------------------------------------
# Util
#-----------------------------------------------------------------

def str_ip_get_version(ip):
    """
    \param ip A string which should contain an IP address
    """
    try: # IPv6 ?
        ip = socket.inet_pton(socket.AF_INET6, ip)
        return socket.AF_INET6
    except socket.error:
        pass
    try: # IPv4 ?
        ip = socket.inet_pton(socket.AF_INET, ip)
        return socket.AF_INET
    except socket.error:
        pass
    raise ValueError(ERR_INVALID_IP % (ip, 0))


