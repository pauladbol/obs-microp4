
/*
 * Author: Myriana Rifai
 * Email: myriana.rifai@nokia-bell-labs.com
 */

#include"msa.p4"
#include"../lib-src/common.p4"

#define TABLE_SIZE 1024

struct sr_meta_t {

}


header ethernet_h {
  bit<48> dmac;
  bit<48> smac;
  bit<16> ethType; 
}


struct sr_hdr_t {
  ethernet_h eth;
}

// need to check the ip header for source routing option
// if option exists then check that the router is in the list of source routing list
// nexthop in the sr list would be the next hop 
cpackage SRv6Main : implements Unicast<sr_hdr_t, sr_meta_t, 
                                     empty_t, empty_t, empty_t> {
  parser micro_parser(extractor ex, pkt p, im_t im, out sr_hdr_t hdr, inout sr_meta_t meta,
                        in empty_t ia, inout empty_t ioa) {          
    state start {
   	  ex.extract(p, hdr.eth);
      transition accept;
    }

   }
  
control micro_control(pkt p, im_t im, inout sr_hdr_t hdr, inout sr_meta_t m,
                          in empty_t ia, out empty_t oa, inout empty_t ioa) {
                          
	IPv6EXT() ipv6Ext_i;
	bit<16> nh;
	action forward(bit<48> dmac, bit<48> smac, PortId_t port) {
      hdr.eth.dmac = dmac;
      hdr.eth.smac = smac;
      im.set_out_port(port);
    }
    table forward_tbl {
      key = { nh : lpm; } 
      actions = { forward; }
    }
    
    apply {
    	if (hdr.eth.ethType == 0x86DD)
    		ipv6Ext_i.apply(p, im, ia, nh, ioa);
      	forward_tbl.apply();
    }
  }
  control micro_deparser(emitter em, pkt p, in sr_hdr_t hdr) {
    apply { 
      em.emit(p, hdr.eth);
    }
  }
}

SRv6Main() main;
