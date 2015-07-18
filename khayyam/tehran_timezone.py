
from datetime import tzinfo, timedelta
from khayyam.jalali_datetime import JalaliDatetime
from khayyam.constants import ZERO_DELTA
from math import floor

STDOFFSET = timedelta(minutes=210) # Minutes
DSTOFFSET = timedelta(minutes=270) # Minutes
DSTDIFF = DSTOFFSET - STDOFFSET


class TehTz(tzinfo):
    
    def utcoffset(self, dt):
        if self._isdst(dt):
            return DSTOFFSET
        else:
            return STDOFFSET
    
    def _isdst(self, dt):
        dt = dt.replace(tzinfo=None)
        if isinstance(dt, JalaliDatetime):
            jdt = dt
        else:
            jdt = JalaliDatetime.from_datetime(dt)
        start_jdt = jdt.replace(month=1, day=1)
        end_jdt = jdt.replace(month=7, day=1)
        if start_jdt < jdt < end_jdt:
            return True
        else:
            return False
    
    def dst(self, dt):
        if self._isdst(dt):
            return DSTDIFF
        else:
            return ZERO_DELTA
                     
    def tzname(self, dt):
        #return 'Iran/Tehran'
        return self.format_offset(dt)
    
    def format_offset(self, dt):
        offset = self.utcoffset(dt)
        return '+%s:%s' % (floor(offset.seconds / 3600), floor((offset.seconds % 3600) / 60))
        
