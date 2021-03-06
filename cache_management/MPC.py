#
from cache_manager import CacheManager

class MPC(CacheManager):
    def _init_strategy(self):
        self.mpc = {}
        for node in self.topology.nodes():
            self.mpc[node] = {}
    def retrieve_from_caches(self, interest, path):
        content_found_caches = False

        for i in range(0, len(path)):
            p = path[i]

            try:
                self.mpc[p][interest]+=1
            except:
                self.mpc[p][interest] = 1

            if self.caches[p].lookup(interest):
                content_found_caches = True
                self.stats.hit()
                break
            else:
                self.stats.miss()

            if content_found_caches and self.mpc[p][interest] >= 1:

                neighbors = self.topology_manager.topology.neighbors(p)
                for n in neighbors:
                    if self.caching_capabilities(n):
                        self.store_cache(n, interest)
                self.mpc[p][interest] = 0
                
        return (content_found_caches, i)
