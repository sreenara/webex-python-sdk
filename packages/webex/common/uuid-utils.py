from base64 import encode, decode

SDK_EVENT = {
  'INTERNAL': {
    'ACTIVITY_TAG': {
      'ONE_ON_ONE': 'ONE_ON_ONE'
    }
  },
  'EXTERNAL': {
    'SPACE_TYPE': {
      'DIRECT': 'DIRECT',
      'GROUP': 'GROUP'
    }
  }
}

hydraTypes = {
  'PEOPLE': 'PEOPLE',
  'ORGANIZATION': 'ORGANIZATION',
  'MESSAGE': 'MESSAGE',
  'ROOM': 'ROOM',
  'MEMBERSHIP': 'MEMBERSHIP',
  'CONTENT': 'CONTENT'
}

INTERNAL_US_CLUSTER_NAME = 'us'
INTERNAL_US_INTEGRATION_CLUSTER_NAME = 'us-integration'

hydraBaseUrl = 'https://api.ciscospark.com/v1'

def isRequired():
  raise Exception('parameter is required')

def constructHydraId(type=isRequired(), id=isRequired(), cluster='us'):
  if not isinstance(type, str):
    raise Exception('"type" must be a string')

  if type == hydraTypes['PEOPLE'] or type == hydraTypes['ORGANIZATION']:
    return encode(f'ciscospark://us/{type}/{id}')

  return encode(f'ciscospark://{cluster}/{type}/{id}')

def deconstructHydraId(id):
  payload = decode(id).split('/')

  return {
    'id': payload.pop(),
    'type': payload.pop(),
    'cluster': payload.pop()
  }

def buildHydraMessageId(uuid, cluster):
  return constructHydraId(hydraTypes['MESSAGE'], uuid, cluster)

def buildHydraPersonId(uuid, cluster):
  return constructHydraId(hydraTypes['PEOPLE'], uuid, cluster)

def buildHydraRoomId(uuid, cluster):
  return constructHydraId(hydraTypes['ROOM'], uuid, cluster)

def buildHydraOrgId(uuid, cluster):
  return constructHydraId(hydraTypes['ORGANIZATION'], uuid, cluster)

def buildHydraMembershipId(personUUID, spaceUUID, cluster):
  return constructHydraId(hydraTypes['MEMBERSHIP'], f'{personUUID}:{spaceUUID}', cluster)

def getHydraClusterString(webex, conversationUrl):
  internalClusterString = webex.internal.services.getClusterId(conversationUrl)

  if internalClusterString.startswith(INTERNAL_US_CLUSTER_NAME) or internalClusterString.startswith(INTERNAL_US_INTEGRATION_CLUSTER_NAME):
    return 'us'

  clusterParts = internalClusterString.split(':')

  if len(clusterParts) < 3:
    raise Exception(f'Unable to determine cluster for convo: {conversationUrl}')

  return f'{clusterParts[0]}:{clusterParts[1]}:{clusterParts[2]}'

def getHydraRoomType(tags):
  if SDK_EVENT['INTERNAL']['ACTIVITY_TAG']['ONE_ON_ONE'] in tags:
    return SDK_EVENT['EXTERNAL']['SPACE_TYPE']['DIRECT']

  return SDK_EVENT['EXTERNAL']['SPACE_TYPE']['GROUP']

def getHydraFiles(activity, cluster):
  hydraFiles = []
  files = activity['object'].get('files')

  if files:
    items = files['items']

    for i in range(len(items)):
      contentId = constructHydraId(hydraTypes['CONTENT'], f'{activity["id"]}/{i}', cluster)
      hydraFiles.append(f'{hydraBaseUrl}/contents/{contentId}')

  return hydraFiles
