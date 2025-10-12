from enum import IntFlag


class ePlaybackState(IntFlag):
    # Base states, each with a unique power-of-two value.
    STOPPED = 0x00
    PLAYING = 0x01
    PAUSED = 0x02
    FAST = 0x04

    # Combined states for more specific conditions.
    FORWARD = PLAYING | 0x08
    BACKWARD = PLAYING | 0x10

    @classmethod
    def IsValid(cls, state: 'ePlaybackState') -> bool:
        """
        Validates if the given state is a valid combination.
        Valid combinations:
        - STOPPED (alone)
        - PAUSED (alone)
        - PLAYING (alone or with FAST)
        - FORWARD (alone or with FAST)
        - BACKWARD (alone or with FAST)
        Invalid if PLAYING and PAUSED are both set, or other conflicting combinations.
        """
        # Check for conflicting flags
        if (state & cls.PLAYING) and (state & cls.PAUSED):
            return False  # Can't be playing and paused

        # Check for valid base combinations
        lBaseState = state & (cls.STOPPED | cls.PLAYING | cls.PAUSED)
        lDirectionFlag = state & (cls.FORWARD | cls.BACKWARD)

        # STOPPED and PAUSED must be alone (no FAST or direction)
        if lBaseState == cls.STOPPED or lBaseState == cls.PAUSED:
            return state == lBaseState

        # PLAYING can be with FAST, but no direction unless specified
        if lBaseState == cls.PLAYING:
            if lDirectionFlag:
                # If direction is set, it must be FORWARD or BACKWARD exactly
                if lDirectionFlag == cls.FORWARD or lDirectionFlag == cls.BACKWARD:
                    return (state & ~(cls.PLAYING | cls.FAST | lDirectionFlag)) == 0
                else:
                    return False
            else:
                # No direction, just PLAYING with optional FAST
                return (state & ~(cls.PLAYING | cls.FAST)) == 0

        return False
