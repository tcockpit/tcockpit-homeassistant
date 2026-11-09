"""Config flow: paste the TCockpit API key from the app (Mehr › Home Assistant)."""
from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import TCockpitApi, TCockpitAuthError, TCockpitError
from .const import CONF_API_KEY, CONF_URL, DEFAULT_URL, DOMAIN


class TCockpitConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def _check(self, key: str, url: str):
        api = TCockpitApi(async_get_clientsession(self.hass), url, key)
        await api.info()
        return await api.vehicles()

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            key = user_input[CONF_API_KEY].strip()
            url = user_input.get(CONF_URL, DEFAULT_URL).strip() or DEFAULT_URL
            try:
                vehicles = await self._check(key, url)
            except TCockpitAuthError:
                errors["base"] = "invalid_auth"
            except TCockpitError:
                errors["base"] = "cannot_connect"
            else:
                await self.async_set_unique_id("tcockpit_" + key[-8:])
                self._abort_if_unique_id_configured()
                title = "TCockpit" + (f" ({', '.join(v['name'] for v in vehicles)})" if vehicles else "")
                return self.async_create_entry(title=title, data={CONF_API_KEY: key, CONF_URL: url})
        schema = vol.Schema({vol.Required(CONF_API_KEY): str, vol.Optional(CONF_URL, default=DEFAULT_URL): str})
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

    async def async_step_reauth(self, entry_data):
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(self, user_input=None):
        errors = {}
        entry = self.hass.config_entries.async_get_entry(self.context["entry_id"])
        if user_input is not None:
            key = user_input[CONF_API_KEY].strip()
            try:
                await self._check(key, entry.data.get(CONF_URL, DEFAULT_URL))
            except TCockpitAuthError:
                errors["base"] = "invalid_auth"
            except TCockpitError:
                errors["base"] = "cannot_connect"
            else:
                self.hass.config_entries.async_update_entry(entry, data={**entry.data, CONF_API_KEY: key})
                await self.hass.config_entries.async_reload(entry.entry_id)
                return self.async_abort(reason="reauth_successful")
        return self.async_show_form(step_id="reauth_confirm", data_schema=vol.Schema({vol.Required(CONF_API_KEY): str}), errors=errors)
