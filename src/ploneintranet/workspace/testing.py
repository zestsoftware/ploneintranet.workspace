from plone.testing import z2

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE

from zope.configuration import xmlconfig


class PloneintranetworkspaceLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import ploneintranet.workspace
        xmlconfig.file(
            'configure.zcml',
            ploneintranet.workspace,
            context=configurationContext
        )
        xmlconfig.includeOverrides(
            configurationContext,
            'overrides.zcml',
            package=ploneintranet.workspace,
        )

        import collective.workspace
        xmlconfig.file(
            'configure.zcml',
            collective.workspace,
            context=configurationContext
        )

        import ploneintranet.invitations
        xmlconfig.file(
            'configure.zcml',
            ploneintranet.invitations,
            context=configurationContext
        )

        import Products.CMFPlacefulWorkflow
        xmlconfig.file(
            'configure.zcml',
            Products.CMFPlacefulWorkflow,
            context=configurationContext
        )

        # Install products that use an old-style initialize() function
        z2.installProduct(app, 'collective.workspace')
        z2.installProduct(app, 'Products.CMFPlacefulWorkflow')

    def tearDownZope(self, app):
        # Uninstall products installed above
        z2.uninstallProduct(app, 'collective.workspace')
        z2.uninstallProduct(app, 'Products.CMFPlacefulWorkflow')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'ploneintranet.workspace:default')

PLONEINTRANET_WORKSPACE_FIXTURE = PloneintranetworkspaceLayer()

PLONEINTRANET_WORKSPACE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PLONEINTRANET_WORKSPACE_FIXTURE,),
    name="PloneintranetworkspaceLayer:Integration"
)
PLONEINTRANET_WORKSPACE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PLONEINTRANET_WORKSPACE_FIXTURE, z2.ZSERVER_FIXTURE),
    name="PloneintranetworkspaceLayer:Functional"
)
PLONEINTRANET_WORKSPACE_ROBOT_TESTING = FunctionalTesting(
    bases=(PLONEINTRANET_WORKSPACE_FIXTURE,
           AUTOLOGIN_LIBRARY_FIXTURE,
           z2.ZSERVER_FIXTURE),
    name="PLONEINTRANET_WORKSPACE_ROBOT")
