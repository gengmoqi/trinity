import enum
from string import Template
from typing import (
    NamedTuple,
)


# Reference: https://github.com/ethereum/eth2.0-specs/blob/dev/specs/networking/p2p-interface.md


#
# Network configuration
#

# The max size of uncompressed gossip messages.
GOSSIP_MAX_SIZE = 2 ** 20  # 1 MiB
# The maximum allowed size of uncompressed req/resp chunked responses.
MAX_CHUNK_SIZE = 2**20  # 1 MiB
# The number of attestation subnets used in the gossipsub protocol.
ATTESTATION_SUBNET_COUNT = 64
# Maximum time to wait for first byte of request response (time-to-first-byte).
TTFB_TIMEOUT = 5  # seconds
# Maximum time for complete response transfer.
RESP_TIMEOUT = 10  # seconds
# The maximum number of slots during which an attestation can be propagated.
ATTESTATION_PROPAGATION_SLOT_RANGE = 32

#
# Gossip domain
#

GOSSIPSUB_PROTOCOL_ID = "/meshsub/1.0.0"


# Parameters
class GossipsubParams(NamedTuple):
    # `D` (topic stable mesh target count)
    DEGREE: int = 6
    # `D_low` (topic stable mesh low watermark)
    DEGREE_LOW: int = 4
    # `D_high` (topic stable mesh high watermark)
    DEGREE_HIGH: int = 12
    # `D_lazy` (gossip target)
    # NOTE: This is the same number as `D` in go-libp2p-pubsub.
    #   Ref: https://github.com/libp2p/go-libp2p-pubsub/blob/5e883d794c9ff281d6ef42d2309dc26532d2d34b/gossipsub.go#L513  # noqa: E501
    DEGREE_LAZY: int = 6
    # `fanout_ttl` (ttl for fanout maps for topics we are not subscribed to
    #   but have published to seconds).
    FANOUT_TTL: int = 60
    # `gossip_advertise` (number of windows to gossip about).
    GOSSIP_WINDOW: int = 3
    # `gossip_history` (number of heartbeat intervals to retain message IDs).
    GOSSIP_HISTORY: int = 5
    # `heartbeat_interval` (frequency of heartbeat, seconds).
    HEARTBEAT_INTERVAL: int = 1  # seconds


# Topics
PUBSUB_TOPIC_BEACON_BLOCK = "beacon_block"
PUBSUB_TOPIC_BEACON_AGGREGATE_AND_PROOF = "beacon_aggregate_and_proof"
PUBSUB_TOPIC_BEACON_ATTESTATION = "beacon_attestation"
PUBSUB_TOPIC_COMMITTEE_BEACON_ATTESTATION = Template(
    "committee_index${subnet_id}_beacon_attestation"
)
PUBSUB_TOPIC_VOLUNTARY_EXIT = "voluntary_exit"
PUBSUB_TOPIC_PROPOSER_SLASHING = "proposer_slashing"
PUBSUB_TOPIC_ATTESTER_SLASHING = "attester_slashing"

PUBSUB_TOPIC_ENCODE_POSTFIX = "ssz"
PUBSUB_TOPIC_ENCODE_COMPRESS_POSTFIX = "ssz_snappy"


#
# Req/Resp domain
#

REQ_RESP_PROTOCOL_PREFIX = "/eth2/beacon_chain/req"


@enum.unique
class ResponseCode(enum.Enum):
    SUCCESS = 0
    INVALID_REQUEST = 1
    SERVER_ERROR = 2


@enum.unique
class GoodbyeReasonCode(enum.IntEnum):
    CLIENT_SHUT_DOWN = 1
    IRRELEVANT_NETWORK = 2
    FAULT_OR_ERROR = 3


REQ_RESP_VERSION = "1"
REQ_RESP_ENCODE_POSTFIX = "ssz"
REQ_RESP_ENCODE_COMPRESS_POSTFIX = "ssz_snappy"
REQ_RESP_STATUS = "status"
REQ_RESP_GOODBYE = "goodbye"
REQ_RESP_BEACON_BLOCKS_BY_RANGE = "beacon_blocks_by_range"
REQ_RESP_BEACON_BLOCKS_BY_ROOT = "beacon_blocks_by_root"
