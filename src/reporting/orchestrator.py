import os
import logging
from .generator import NotebookGenerator

class Phase4Orchestrator:
    def __init__(self, project_root):
        self.project_root = project_root
        self.logger = logging.getLogger(__name__)
        self.generator = NotebookGenerator()
        
        self.templates = {
            "4_1_methodology": "academic/methodological_report/phase4_4_1_metodologia_eda.ipynb",
            "4_2_math": "academic/methodological_report/phase4_4_2_matematicas_eda.ipynb",
            "4_3_results": "academic/methodological_report/phase4_4_3_resultados_eda.ipynb",
            "4_4_interpretation": "academic/methodological_report/phase4_4_4_interpretacion_eda.ipynb",
            "general_report": "academic/Reporte_Integral_TFM (Actualizado).ipynb"
        }

    def _to_forward_slash(self, path):
        """
        Converts Windows backslashes to forward slashes.
        Prevents SyntaxError when paths are injected into notebook cells,
        where \\U, \\P, \\T etc. would be interpreted as unicode escapes.
        Python on Windows accepts forward slashes in all file operations.
        """
        return path.replace('\\', '/')

    def generate_reports(self, phase3_csv_path, output_dir_base, anchors_json_path=None):
        """
        Generates all Phase 4 notebooks using the provided Phase 3 data.

        Args:
            phase3_csv_path (str): Absolute path to phase3_results.csv
            output_dir_base (str): Absolute path to output directory.
            anchors_json_path (str, optional): Path to dimensions/anchors JSON file.
        """
        phase3_csv_path = os.path.abspath(phase3_csv_path)
        output_dir_base = os.path.abspath(output_dir_base)

        self.logger.info(f"Starting Phase 4 report generation. Output: {output_dir_base}")

        if not os.path.exists(phase3_csv_path):
            self.logger.error(f"Phase 3 CSV not found at {phase3_csv_path}")
            raise FileNotFoundError(f"Phase 3 CSV not found at {phase3_csv_path}")

        os.makedirs(output_dir_base, exist_ok=True)

        # ── Derive all companion paths from phase3 CSV location ──────────────
        # Structure expected:
        #   results/phase3/mh_strict_.../phase3_results.csv
        #   results/phase3/mh_strict_.../artifacts/
        #   results/phase3/mh_strict_.../artifacts/anchors/   <-- .npz computed anchors
        #   results/phase3/mh_strict_.../artifacts/subspaces/
        phase3_dir    = os.path.dirname(phase3_csv_path)
        artifacts_dir = os.path.join(phase3_dir, "artifacts")
        anchors_dir   = os.path.join(phase3_dir, "artifacts", "anchors")
        subspaces_dir = os.path.join(phase3_dir, "artifacts", "subspaces")

        if not os.path.exists(subspaces_dir):
            subspaces_dir = os.path.join(self.project_root, "data", "phase3", "artifacts", "subspaces")

        self.logger.info(f"phase3_dir    : {phase3_dir}")
        self.logger.info(f"artifacts_dir : {artifacts_dir}")
        self.logger.info(f"anchors_dir   : {anchors_dir}")
        self.logger.info(f"subspaces_dir : {subspaces_dir}")

        # ── Build replacements — all paths use forward slashes ───────────────
        # ANCHORS_DIR is the key fix: this is what General_Report uses to load
        # the .npz anchor embedding files like anchors_baseline_penultimate_corrected.npz
        replacements = {
            "PHASE3_CSV":    f"'{self._to_forward_slash(phase3_csv_path)}'",
            "CSV_PATH":      f"'{self._to_forward_slash(phase3_csv_path)}'",
            "ARTIFACTS_DIR": f"'{self._to_forward_slash(artifacts_dir)}'",
            "ANCHORS_DIR":   f"'{self._to_forward_slash(anchors_dir)}'",
            "base_dir":      f"'{self._to_forward_slash(subspaces_dir)}'",
        }

        # ── Find ANCHORS_CSV (embeddings_anchors.csv) ────────────────────────
        possible_anchors_names = [
            "embeddings_anchors.csv",
            "anchors_matrix.csv",
            "anchors.csv",
        ]
        possible_anchors_dirs = [
            artifacts_dir,
            anchors_dir,
            phase3_dir,
            os.path.join(self.project_root, "data"),
        ]

        found_anchor = False
        for d in possible_anchors_dirs:
            if found_anchor:
                break
            if not os.path.exists(d):
                continue
            for name in possible_anchors_names:
                p = os.path.join(d, name)
                if os.path.exists(p):
                    replacements["ANCHORS_CSV"] = f"'{self._to_forward_slash(p)}'"
                    self.logger.info(f"Found ANCHORS_CSV: {p}")
                    found_anchor = True
                    break

        if not found_anchor:
            self.logger.warning("ANCHORS_CSV not found. Notebooks requiring it may fail.")

        # ── Find DIMENSIONS_JSON ─────────────────────────────────────────────
        # Note: DIMENSIONS_JSON is your hand-crafted anchor definitions file
        #       (data/metadata/anchors/dimensiones_ancla_mh_es_covid_FSA_ascii.json)
        #       It is DIFFERENT from ANCHORS_DIR which contains the computed .npz files.
        if anchors_json_path and os.path.exists(anchors_json_path):
            replacements["DIMENSIONS_JSON"] = f"'{self._to_forward_slash(os.path.abspath(anchors_json_path))}'"
            self.logger.info(f"Using provided DIMENSIONS_JSON: {anchors_json_path}")
        else:
            possible_dims_names = [
                "dimensiones_ancla_mh_es_covid_FSA_ascii.json",
                "dimensiones_ancla_mh_es_covid.json",
                "dimensiones_ancla.json",
                "dimensions.json",
                "anchors.json",
            ]
            possible_dims_dirs = [
                os.path.join(self.project_root, "data", "metadata", "anchors"),
                os.path.join(self.project_root, "data", "metadata"),
                os.path.join(self.project_root, "configs"),
                phase3_dir,
                artifacts_dir,
                anchors_dir,
                os.path.join(self.project_root, "data"),
            ]

            found_dim = False
            for d in possible_dims_dirs:
                if found_dim:
                    break
                if not os.path.exists(d):
                    continue
                for name in possible_dims_names:
                    p = os.path.join(d, name)
                    if os.path.exists(p):
                        replacements["DIMENSIONS_JSON"] = f"'{self._to_forward_slash(p)}'"
                        self.logger.info(f"Found DIMENSIONS_JSON: {p}")
                        found_dim = True
                        break

            if not found_dim:
                self.logger.warning(
                    "DIMENSIONS_JSON not found in any standard location. "
                    "Pass --anchors to specify it explicitly."
                )

        # ── Find MANIFEST_JSON ───────────────────────────────────────────────
        for manifest_name in ["manifest.json", "run_manifest.json"]:
            manifest_path = os.path.join(phase3_dir, manifest_name)
            if not os.path.exists(manifest_path):
                manifest_path = os.path.join(artifacts_dir, "manifests", manifest_name)
            if os.path.exists(manifest_path):
                replacements["MANIFEST_JSON"] = f"'{self._to_forward_slash(manifest_path)}'"
                self.logger.info(f"Found MANIFEST_JSON: {manifest_path}")
                break

        # ── Fix sys.path.append — use forward slashes to avoid unicode escape ─
        safe_project_root = self._to_forward_slash(self.project_root)
        replacements["sys.path.append('..')"] = f"sys.path.append('{safe_project_root}')"

        # ── Log final replacements for debugging ─────────────────────────────
        self.logger.info("Replacements injected into notebooks:")
        for k, v in replacements.items():
            self.logger.info(f"  {k} = {v}")

        # ── Output artifacts folder ──────────────────────────────────────────
        os.makedirs(os.path.join(output_dir_base, "artifacts"), exist_ok=True)

        # ── Generate each notebook ───────────────────────────────────────────
        for key, relative_template_path in self.templates.items():
            template_full_path = os.path.join(self.project_root, relative_template_path)

            if not os.path.exists(template_full_path):
                self.logger.warning(f"Template not found: {template_full_path}. Skipping.")
                continue

            output_filename = "General_Report.ipynb" if key == "general_report" \
                              else os.path.basename(relative_template_path)
            output_full_path = os.path.join(output_dir_base, output_filename)

            self.logger.info(f"Generating {key} -> {output_full_path}")

            try:
                self.generator.generate_and_execute(
                    template_path=template_full_path,
                    output_path=output_full_path,
                    replacements=replacements
                )
                self.logger.info(f"Successfully generated {output_filename}")
            except Exception as e:
                self.logger.error(f"Failed to generate {output_filename}: {e}")