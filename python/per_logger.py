#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2015 <+YOU OR YOUR COMPANY+>.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

import numpy
from gnuradio import gr
from gnuradio import digital
import pmt
import string
import time
import csv

class per_logger(gr.basic_block):
    """
    docstring for block per_logger
    """
    def __init__(self):
        gr.basic_block.__init__(self,
            name="per_logger",
            in_sig=[],
            out_sig=[])

        self.message_port_register_in(pmt.intern('payload_in'))
        self.set_msg_handler(pmt.intern('payload_in'), self.handle_payload_message)
        self.message_port_register_in(pmt.intern('snr_in'))
        self.set_msg_handler(pmt.intern('snr_in'), self.handle_snr_message)

        self.csv_fields = ['Timestamp', 'OK', 'SNR']
        self.log_file_name = '/home/inets/per_log.csv'

        with open(self.log_file_name,'w') as log_file:
            csv_writer = csv.DictWriter(log_file, fieldnames=self.csv_fields)
            csv_writer.writeheader()
        
        self.csv_fields_stats = ['Timestamp', 'SNR', 'PER']
        self.stats_log_file_name = '/home/inets/per_stats_log.csv'

        with open(self.stats_log_file_name,'w') as log_file:
            csv_writer = csv.DictWriter(log_file, fieldnames=self.csv_fields_stats)
            csv_writer.writeheader()

        self.log = False
        self.curr_snr = 0
        self.num_rec_packets = 0
        self.avg_snr = 0
        self.num_packet_errors = 0

        numpy.random.seed(0)
        self.payload = numpy.random.randint(0, 256, 500) #500 byte payload
        print '[per_logger] using payload:'
        print self.payload

    def handle_payload_message(self, msg_pmt):
        if not self.log:
            return

        meta = pmt.to_python(pmt.car(msg_pmt))
        msg = pmt.cdr(msg_pmt)
        msg_data = pmt.u8vector_elements(msg)

        self.num_rec_packets += 1
        self.avg_snr += self.curr_snr
        ok = True
        
        print '[per_logger] got message. Total = ' + str(self.num_rec_packets)
        #print list(msg_data)
        
        bit_errors = self.compare_lists(list(msg_data), self.payload)

        if  bit_errors > 0:
            self.num_packet_errors += 1
            print '[per_logger] Packet error. Byte errors = ' + str(bit_errors)
            ok = False

        self.log_packet(ok, self.curr_snr)

        if self.num_rec_packets == 10000:
            snr = sefl.avg_snr / self.num_rec_packets
            per = self.num_packet_errors / self.num_rec_packets
            self.num_rec_packets = 0
            self.avg_snr = 0
            self.log = False
            self.log_stats(snr, per)

    def log_packet(self, ok, snr):
        with open(self.log_file_name, 'a') as log_file:
            csv_writer = csv.DictWriter(log_file, fieldnames=self.csv_fields)
            csv_writer.writerow({'Timestamp' : time.time(),
                    'OK' : ok,
                    'SNR' : snr})

    def log_stats(self, ok, snr):
        with open(self.stats_log_file_name, 'a') as log_file:
            csv_writer = csv.DictWriter(log_file, fieldnames=self.csv_fields_stats)
            csv_writer.writerow({'Timestamp' : time.time(),
                    'SNR' : snr,
                    'PER' : per})

    def handle_snr_message(self, msg):
        snr_pmt = pmt.to_python(msg)
        snr = float(snr_pmt)
        self.curr_snr = snr
        self.log = True

    def compare_lists(self, list1, list2):
        byte_errors = 0
        for  x, y in zip(list1,list2):
            if x != y:
                byte_errors += 1

        return byte_errors

         