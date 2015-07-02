/* -*- c++ -*- */
/* 
 * Copyright 2015 <+YOU OR YOUR COMPANY+>.
 * 
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifndef INCLUDED_INETS_FRAME_SYNC_CC_IMPL_H
#define INCLUDED_INETS_FRAME_SYNC_CC_IMPL_H

#include <inets/frame_sync_cc.h>

namespace gr {
  namespace inets {

    class frame_sync_cc_impl : public frame_sync_cc
    {
      private:
		    std::vector<gr_complex> _preamble; //13 bit Barker code
		    float _threshold;
		    int _len_preamble;
		    std::string _len_tag_key;
	    	int _state;
		    float _d_f;
        float _d_phi;
        float _last_corr;
        std::complex<float> _diff;
        static const int STATE_DETECT = 0;
		    static const int STATE_PREAMBLE = 1;
		    static const int STATE_PAYLOAD = 3;
		    static const int STATE_PROCESS_PREAMBLE = 2;
        static const int STATE_SET_TRIGGER = 4;
        
        float calculate_fd(const gr_complex* x, const gr_complex* c, int N, int L0);
        std::complex<double> calculate_R(int m, const std::complex<double>* z, int L0);
        float wrap_phase(float phi);
      public:
        frame_sync_cc_impl(float threshold, const std::string &len_tag_key);
        ~frame_sync_cc_impl();
	      void forecast(int noutput_items, gr_vector_int &ninput_items_required);
        // Where all the action really happens
        int general_work(int noutput_items,
		      gr_vector_int &ninput_items,
	        gr_vector_const_void_star &input_items,
	        gr_vector_void_star &output_items);
    };

  } // namespace inets
} // namespace gr

#endif /* INCLUDED_INETS_FRAME_SYNC_CC_IMPL_H */ 